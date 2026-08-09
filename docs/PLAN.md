# PingPal — Implementation Plan

## Overview

PingPal is a lightweight home network monitoring tool. The goal is a **Green/Yellow/Red** health dashboard accessible via web browser and native Android, with real-time device discovery and internet latency tracking.

## Phases

### Phase 1: Python Network Core ✅

**Goal**: Standalone ARP scanning and async latency tracking — no server, no UI.

- [x] `scanner.py`: Scapy ARP sweep across configured subnet, return MAC + IP pairs
- [x] `tracker.py`: Async HTTPX loop pinging external targets (1.1.1.1, 8.8.8.8), record latency + packet loss
- [x] `database.py`: SQLite schema for `devices` and `outage_log` tables
- [x] `config.py`: Subnet CIDR, ping interval (default 5s), thresholds, external targets

**Deliverable**: Run `scanner.py` and `tracker.py` independently, see output on stdout.

---

### Phase 2: Real-time Backend Engine ✅

**Goal**: FastAPI server with WebSocket broadcasts, persistence, and webhook alerts.

- [x] `main.py`: FastAPI app + python-socketio server on same port
- [x] Socket.IO events: `device_list`, `device_update`, `latency_update`, `new_device_alert`, `outage_alert`
- [x] Background tasks: scanner loop and tracker loop run as asyncio tasks on startup
- [x] `database.py`: full CRUD — insert/update devices, log outages, persist nicknames
- [x] `notifier.py`: Discord and Telegram webhook dispatchers for new device alerts
- [x] REST endpoints: `GET /api/devices`, `GET /api/status`, `POST /api/devices/:mac/label`

**Deliverable**: Backend serves API + WebSocket. Connect a raw Socket.IO client, receive live events.

---

### Phase 3: React + TypeScript Web Dashboard ✅

**Goal**: Mobile-friendly web UI with real-time health cards, device list, and latency chart.

- [x] Vite + React 18 + TypeScript project scaffold (`frontend/`)
- [x] `socket.ts`: Socket.IO client connection manager with auto-reconnect
- [x] `NetworkStatus.tsx`: Green/Yellow/Red badge driven by `latency_update` events
- [x] `DeviceCard.tsx` + `DeviceList.tsx`: Scrollable device grid with MAC, IP, label, online/offline
- [x] `LatencyChart.tsx`: Real-time scrolling line chart (lightweight canvas or Recharts)
- [x] `AlertBanner.tsx`: Toast notifications for new devices and outages
- [x] `Layout.tsx`: App shell with header, nav, and responsive content area
- [x] Custom hooks: `useDevices`, `useLatency`, `useAlerts` for socket state
- [x] Dark mode CSS variables + mobile-first styles

**Deliverable**: Open `http://localhost:5173`, see live dashboard updating from backend.

---

### Phase 4: Mobile Compilation 🔲

**Goal**: Package the React UI as a native Android app via Capacitor.

- [ ] Add Capacitor to frontend project, configure `capacitor.config.ts`
- [ ] Verify network permissions in `AndroidManifest.xml` (INTERNET, ACCESS_NETWORK_STATE, ACCESS_WIFI_STATE)
- [ ] Test on Android emulator and physical device
- [ ] Handle Android lifecycle (app background → socket reconnect)
- [ ] Generate signed APK for distribution

**Deliverable**: `.apk` installs on Android, connects to backend, shows live dashboard.

---

### Phase 5: Push Notifications & Webhooks 🔲

**Goal**: Native Android push notifications for new-device alerts + configurable webhook routing.

- [ ] Capacitor Push Notifications plugin integration
- [ ] Firebase Cloud Messaging (FCM) setup for Android push
- [ ] Backend: store device push tokens, dispatch on alert events
- [ ] Webhook configuration UI in dashboard (add/remove Discord/Telegram URLs)
- [ ] Rate-limiting on alerts (no more than 1 per 60s per device)

**Deliverable**: Phone buzzes when unknown device joins Wi-Fi. Webhooks fire to configured URLs.

---

## Tech Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Backend framework | FastAPI | Async-native, auto OpenAPI docs, good WebSocket support via python-socketio |
| Device discovery | Scapy ARP | Works on all OSes, no external deps beyond Python, reliable on home subnets |
| Latency tracking | HTTPX (async) | Same library for pings AND webhook POSTs, single dependency |
| Database | SQLite + aiosqlite | Zero-config, single file, enough for home use (<100 devices) |
| Real-time transport | Socket.IO | Auto-reconnect, fallback to long-polling, room support, widely supported |
| Frontend framework | React 18 + Vite | Fast dev server, TypeScript out of box, large ecosystem |
| Mobile packaging | Capacitor | Single codebase for web + Android, no need for React Native rewrite |
| Charts | Recharts (or lightweight canvas) | React-native, small bundle, good for real-time updates |

## Milestones

```
Phase 1  ████████████  Done
Phase 2  ████████████  Done
Phase 3  ████████████  Done
Phase 4  ░░░░░░░░░░░░  Not started
Phase 5  ░░░░░░░░░░░░  Not started
```

## Dependencies Between Phases

```
Phase 1 ──► Phase 2 ──► Phase 3 ──► Phase 4
                          │
                          └──► Phase 5 (can overlap with Phase 4)
```

- Phase 2 depends on Phase 1 (needs scanner + tracker modules)
- Phase 3 depends on Phase 2 (needs WebSocket server to connect to)
- Phase 4 depends on Phase 3 (wraps the built React app)
- Phase 5 depends on Phase 3 (needs UI for webhook config) and Phase 4 (for native push)

## Risk Register

| Risk | Impact | Mitigation |
|------|--------|------------|
| Scapy requires root/sudo on Linux | Dev friction | Document clearly; consider fallback to `arp -a` parsing |
| ARP scan misses devices in sleep mode | False negatives | Periodic re-scan (every 60s); show "last seen" timestamp |
| Cross-origin Socket.IO from Capacitor WebView | Connection failures | CORS config on backend; Capacitor `allowNavigation` rules |
| FCM setup complexity for Phase 5 | Delayed delivery | Start FCM config early; test with simple ping before full integration |
