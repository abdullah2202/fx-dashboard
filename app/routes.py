from datetime import datetime, date
from flask import Blueprint, request, jsonify, render_template
from sqlalchemy import func
from app import db
from app.models import Event, Candle

bp = Blueprint('main', __name__)


@bp.route('/')
def dashboard():
    """Serve the dashboard page."""
    return render_template('dashboard.html')


@bp.route('/api/event', methods=['POST'])
def log_event():
    """Receive and store an event log from a trading bot."""
    data = request.get_json()
    
    if not data:
        return jsonify({'status': 'error', 'message': 'No JSON data provided'}), 400
    
    required_fields = ['bot_id', 'event_type']
    for field in required_fields:
        if field not in data:
            return jsonify({'status': 'error', 'message': f'Missing required field: {field}'}), 400
    
    # Parse timestamp or use current time
    timestamp = datetime.utcnow()
    if 'timestamp' in data:
        try:
            timestamp = datetime.fromisoformat(data['timestamp'].replace('Z', '+00:00'))
        except ValueError:
            pass
    
    event = Event(
        bot_id=data['bot_id'],
        timestamp=timestamp,
        event_type=data['event_type'],
        details=data.get('details')
    )
    
    db.session.add(event)
    db.session.commit()
    
    return jsonify({'status': 'success', 'id': event.id}), 201


@bp.route('/api/candle', methods=['POST'])
def log_candle():
    """Receive and store a candle log from a trading bot."""
    data = request.get_json()
    
    if not data:
        return jsonify({'status': 'error', 'message': 'No JSON data provided'}), 400
    
    required_fields = ['bot_id', 'timestamp', 'open', 'high', 'low', 'close']
    for field in required_fields:
        if field not in data:
            return jsonify({'status': 'error', 'message': f'Missing required field: {field}'}), 400
    
    # Parse timestamp
    try:
        timestamp = datetime.fromisoformat(data['timestamp'].replace('Z', '+00:00'))
    except ValueError:
        return jsonify({'status': 'error', 'message': 'Invalid timestamp format. Use ISO format.'}), 400
        
    candle = Candle(
        bot_id=data['bot_id'],
        timestamp=timestamp,
        open=float(data['open']),
        high=float(data['high']),
        low=float(data['low']),
        close=float(data['close']),
        volume=float(data.get('volume', 0.0))
    )
    
    db.session.add(candle)
    db.session.commit()
    
    return jsonify({'status': 'success', 'id': candle.id}), 201


@bp.route('/api/candles', methods=['GET'])
def get_candles():
    """Get recent candles."""
    limit = request.args.get('limit', 100, type=int)
    bot_id = request.args.get('bot_id')
    
    query = Candle.query.order_by(Candle.timestamp.desc())
    
    if bot_id:
        query = query.filter(Candle.bot_id == bot_id)
    
    candles = query.limit(limit).all()
    # Return in chronological order
    return jsonify([c.to_dict() for c in reversed(candles)])


@bp.route('/api/events', methods=['GET'])
def get_events():
    """Get recent events for the live feed."""
    limit = request.args.get('limit', 50, type=int)
    bot_id = request.args.get('bot_id')
    
    query = Event.query.order_by(Event.timestamp.desc())
    
    if bot_id:
        query = query.filter(Event.bot_id == bot_id)
    
    events = query.limit(limit).all()
    return jsonify([e.to_dict() for e in events])


@bp.route('/api/summary', methods=['GET'])
def get_summary():
    """Get aggregated stats (PnL, Win Rate) filtered by Bot ID or Date."""
    bot_id = request.args.get('bot_id')
    date_str = request.args.get('date')
    
    # Default to today
    target_date = date.today()
    if date_str:
        try:
            target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'status': 'error', 'message': 'Invalid date format. Use YYYY-MM-DD'}), 400
    
    # Build base query for the target date
    query = Event.query.filter(
        func.date(Event.timestamp) == target_date
    )
    
    if bot_id:
        query = query.filter(Event.bot_id == bot_id)
    
    events = query.all()
    
    # Aggregate stats per bot
    bots = {}
    for event in events:
        if event.bot_id not in bots:
            bots[event.bot_id] = {
                'bot_id': event.bot_id,
                'total_events': 0,
                'entries': 0,
                'exits': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'total_pnl': 0.0
            }
        
        bot_stats = bots[event.bot_id]
        bot_stats['total_events'] += 1
        
        if event.event_type == 'ENTRY':
            bot_stats['entries'] += 1
        elif event.event_type == 'EXIT':
            bot_stats['exits'] += 1
            # Extract PnL from details if available
            if event.details and 'pnl' in event.details:
                pnl = float(event.details['pnl'])
                bot_stats['total_pnl'] += pnl
                if pnl > 0:
                    bot_stats['winning_trades'] += 1
                else:
                    bot_stats['losing_trades'] += 1
    
    # Calculate win rates
    summaries = []
    for bot_id, stats in bots.items():
        total_trades = stats['winning_trades'] + stats['losing_trades']
        stats['win_rate'] = round((stats['winning_trades'] / total_trades * 100), 2) if total_trades > 0 else 0
        stats['total_pnl'] = round(stats['total_pnl'], 2)
        summaries.append(stats)
    
    return jsonify({
        'date': target_date.isoformat(),
        'bots': summaries
    })
