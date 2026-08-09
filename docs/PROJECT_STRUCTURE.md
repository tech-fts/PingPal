# PingPal — Project Structure

```
pingpal/
├── README.md                         # Project overview, features, tech stack
├── LICENSE                           # MIT License
├── docs/
│   ├── PROJECT_STRUCTURE.md          # This file — full tree + component map
│   └── PLAN.md                       # Implementation plan with phases & milestones
│
├── backend/                          # Python FastAPI + Socket.IO engine
│   ├── requirements.txt              # Python dependencies
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                   # FastAPI app entry point, Socket.IO server init
│   │   ├── config.py                 # Subnet, ping thresholds, env settings
│   │   ├── scanner.py                # Scapy ARP network sweep, MAC discovery
│   │   ├── tracker.py                # Async HTTPX latency ping loops
│   │   ├── notifier.py               # Discord / Telegram webhook dispatchers
│   │   └── database.py               # SQLite interface for known devices & history
│   └── tests/
│       ├── __init__.py
│       ├── test_scanner.py
│       ├── test_tracker.py
│       ├── test_notifier.py
│       └── test_database.py
│
└── frontend/                         # React + TypeScript cross-platform client
    ├── package.json
    ├── tsconfig.json
    ├── vite.config.ts
    ├── capacitor.config.ts           # Capacitor native platform config
    ├── index.html
    ├── public/
    │   └── favicon.svg
    ├── src/
    │   ├── main.tsx                  # React entry point
    │   ├── App.tsx                   # Root component, layout shell
    │   ├── components/
    │   │   ├── NetworkStatus.tsx     # Green/Yellow/Red health indicator
    │   │   ├── DeviceCard.tsx        # Individual device row (MAC, label, status)
    │   │   ├── DeviceList.tsx        # Scrollable device list container
    │   │   ├── LatencyChart.tsx      # Real-time latency graph
    │   │   ├── AlertBanner.tsx       # New-device and outage notifications
    │   │   └── Layout.tsx            # App shell: header, nav, content area
    │   ├── services/
    │   │   └── socket.ts             # Socket.IO client connection manager
    │   ├── types/
    │   │   └── index.ts              # TS interfaces: Device, NetworkStatus, AlertEvent
    │   ├── hooks/
    │   │   ├── useDevices.ts         # Device list state + socket subscription
    │   │   ├── useLatency.ts         # Latency data stream hook
    │   │   └── useAlerts.ts          # New-device and outage alert state
    │   └── styles/
    │       └── index.css             # Global styles, CSS variables, dark mode
    ├── android/                      # Capacitor native Android workspace (generated)
    └── tests/
        └── components/
            ├── NetworkStatus.test.tsx
            └── DeviceCard.test.tsx
```

## Component Map

### Backend (Python)

| Module | Responsibility | Key Dependencies |
|--------|---------------|-----------------|
| `main.py` | FastAPI app, Socket.IO server, route registration, CORS | FastAPI, python-socketio |
| `config.py` | Subnet CIDR, ping interval, thresholds, webhook URLs | pydantic-settings |
| `scanner.py` | ARP sweep subnet → MAC + IP list, device fingerprinting | Scapy |
| `tracker.py` | Async ping loop → latency + packet loss per target | HTTPX, asyncio |
| `database.py` | SQLite CRUD: known devices, nicknames, outage history | aiosqlite |
| `notifier.py` | Outgoing webhook POSTs to Discord/Telegram on events | HTTPX |

### Frontend (React + TypeScript)

| Component | Responsibility | Socket Events Consumed |
|-----------|---------------|----------------------|
| `NetworkStatus` | Green/Yellow/Red badge + latest latency/packet loss | `latency_update` |
| `DeviceList` | Scrollable list of all known devices | `device_list`, `device_update` |
| `DeviceCard` | Single device: MAC, IP, label, vendor, online/offline | — (prop-driven) |
| `LatencyChart` | Real-time scrolling line chart of ping history | `latency_update` |
| `AlertBanner` | Toast-style alerts for new devices, outages | `new_device_alert`, `outage_alert` |
| `Layout` | App shell: header, nav tabs, content slot | — |

### Data Flow

```
Home WiFi Subnet
      │
      ▼ (ARP / ICMP)
[scanner.py] ──► device_list ──► [database.py] ──► SQLite
                                         │
[tracker.py] ──► latency_update ─────────┤
                                         │
                              [python-socketio Server]
                                         │
                              WebSocket (Socket.IO)
                                         │
                    ┌────────────────────┴────────────────────┐
                    ▼                                         ▼
           [React Web UI]                          [Android (Capacitor)]
```

### Key Socket.IO Events

| Event | Direction | Payload |
|-------|-----------|---------|
| `device_list` | Server → Client | `Device[]` — full list on connect |
| `device_update` | Server → Client | `Device` — single device changed |
| `latency_update` | Server → Client | `{ timestamp, latency_ms, packet_loss }` |
| `new_device_alert` | Server → Client | `Device` — unrecognized MAC detected |
| `outage_alert` | Server → Client | `{ start, duration, targets[] }` |
| `label_device` | Client → Server | `{ mac, nickname }` — user renames device |
