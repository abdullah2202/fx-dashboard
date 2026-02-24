# Trading Dashboard & Logger API

A Flask-based API for trading bots to log events, with a real-time dashboard to monitor performance.

[//]: # ![Dashboard Screenshot](https://github.com/abdullah2202/fx-dashboard/raw/main/docs/dashboard.png)

## Features

- **Event Logging API** - Receive and store trading events (SETUP, ENTRY, EXIT, UPDATE)
- **Live Dashboard** - Real-time feed of incoming events with auto-refresh
- **Performance Summary** - Aggregated stats per bot (PnL, Win Rate, Entries/Exits)
- **Docker Ready** - Production-ready with Docker Compose

## Quick Start

```bash
# Clone the repository
git clone https://github.com/abdullah2202/fx-dashboard.git
cd fx-dashboard

# Run with Docker
docker-compose up --build -d
```

Access the dashboard at **http://localhost:5000**

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Dashboard UI |
| `/api/event` | POST | Log a trading event |
| `/api/events` | GET | Get recent events |
| `/api/summary` | GET | Get aggregated stats |

### Log an Event

```bash
curl -X POST http://localhost:5000/api/event \
  -H "Content-Type: application/json" \
  -d '{
    "bot_id": "gold-breaking",
    "timestamp": "2026-02-03T14:00:00Z",
    "event_type": "ENTRY",
    "details": {"pair": "XAU/USD", "price": 2050.50}
  }'
```

**Response:** `{"id": 1, "status": "success"}`

### Event Types

| Type | Description |
|------|-------------|
| `SETUP` | Bot initialization or configuration |
| `ENTRY` | Opening a trade |
| `EXIT` | Closing a trade (include `pnl` in details) |
| `UPDATE` | Status updates |

### Get Summary

```bash
curl http://localhost:5000/api/summary
curl http://localhost:5000/api/summary?bot_id=gold-breaking
curl http://localhost:5000/api/summary?date=2026-02-03
```

## Configuration

Environment variables (set in `docker-compose.yml`):

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | SQLite database path | `sqlite:////data/trading.db` |
| `SECRET_KEY` | Flask secret key | Required |

## Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run locally
python run.py
```

## Tech Stack

- **Backend:** Flask, Flask-SQLAlchemy
- **Database:** SQLite
- **Frontend:** Bootstrap 5, Vanilla JS
- **Deployment:** Docker, Gunicorn

## License

MIT
