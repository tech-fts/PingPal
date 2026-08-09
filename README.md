# 📡 PingPal — Home Wi-Fi & Internet Stability Companion

> A lightweight, consumer-friendly network monitoring tool designed to track Wi-Fi health, flag internet lag, and alert you when new devices join your home network.

---

## 💡 Overview

Enterprise networking tools like Wireshark or Nagios are far too complex for everyday home users. **PingPal** simplifies home network monitoring into a clean, intuitive "Green/Yellow/Red" status dashboard accessible on both Web browsers and native Android devices.

---

## ✨ Core Features

* **Local Device Radar**: Periodically scans your home Wi-Fi network using lightweight ARP requests to discover connected devices (phones, laptops, smart TVs, consoles) and assigns friendly labels.
* **Internet Health & Lag Tracker**: Continuously measures latency and packet loss in the background using asynchronous pings to log network slowdowns and outages.
* **New Device Alerts**: Instantly triggers webhooks (Discord, Telegram) or system alerts whenever an unrecognized device connects to your subnet.
* **Real-Time Cross-Platform Dashboard**: Mobile-friendly UI built with React and TypeScript, streaming real-time status updates and performance charts over WebSockets.

---

## 🛠️ Tech Stack

### Backend Engine (Python)

| Tool / Library | Role | Why It's Used |
| --- | --- | --- |
| **Python 3.10+** | Runtime | Asynchronous core engine for network scanning and monitoring. |
| **FastAPI** | Web Framework | Lightweight, high-performance API server. |
| **python-socketio** | WebSocket Server | Pushes live connection events and latency updates to connected clients instantly. |
| **Scapy / Socket** | Device Discovery | Executes ARP sweeps and TCP probing across the local subnet to detect MAC addresses. |
| **HTTPX** | Latency & Webhooks | Asynchronously checks external server response times and sends outgoing alert webhooks. |
| **SQLite** | Local Storage | Persists known device profiles, custom nicknames, and network outage history. |

### Frontend & Mobile Client (React + TypeScript)

| Tool / Library | Role | Why It's Used |
| --- | --- | --- |
| **React 18** | UI Library | Component-driven architecture for rendering dashboard states and device lists. |
| **TypeScript** | Type Safety | Strictly types network events, device status payloads, and Socket.IO messages. |
| **Socket.IO Client** | Real-Time Sync | Maintains active WebSocket connection to stream live metrics from the Python backend. |
| **Capacitor** | Native Android Bridge | Packages the React TypeScript frontend into a native Android app without code duplication. |
| **Vite** | Frontend Bundler | Fast development server and optimized build tool. |

---

## 🏗️ Architecture Breakdown

```text
 [ Home Wi-Fi Subnet ] <---(ARP / Socket Scans)---> [ Python Backend (FastAPI) ]
                                                            │
 [ External Targets  ] <---(Async HTTP via HTTPX)-----------┤
                                                            │ (WebSocket Events)
                                                    [ python-socketio ]
                                                            │
                                        ┌───────────────────┴───────────────────┐
                                        ▼                                       ▼
                             [ React + TS Web UI ]                  [ Android App (Capacitor) ]

```

---

## 📂 Project Structure

```text
pingpal/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app & Socket.io server initialization
│   │   ├── config.py            # Subnet definition, ping thresholds, settings
│   │   ├── scanner.py           # Scapy ARP network sweep & MAC address discovery
│   │   ├── tracker.py           # Asynchronous HTTPX latency ping loops
│   │   ├── notifier.py          # Discord/Telegram webhook dispatchers
│   │   └── database.py          # SQLite database interface for known devices
│   └── requirements.txt         # Backend dependencies
│
└── frontend/                    # Cross-Platform React + TypeScript Client
    ├── src/
    │   ├── components/          # NetworkStatus, DeviceCard, LatencyChart
    │   ├── services/            # Socket.io connection manager
    │   ├── types/               # TypeScript interfaces for network payloads
    │   ├── App.tsx              # Main dashboard view
    │   └── main.tsx             # Application entry point
    ├── android/                 # Capacitor native Android workspace
    ├── capacitor.config.ts      # Native platform configuration
    ├── package.json
    └── vite.config.ts

```

---

## 🚀 Getting Started

### Prerequisites

* **Python 3.10+**
* **Node.js 18+** & `npm`
* **Android Studio** *(Optional: Only needed if compiling the native `.apk`)*
* **Administrator / Root Privileges**: Scapy requires elevated network privileges (`sudo` on Linux/macOS or Administrator on Windows) to send raw ARP packets.

---

### 1. Backend Setup (Python)

```bash
# Navigate to backend
cd pingpal/backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run backend with elevated permissions (required for Scapy ARP access)
sudo ./venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

```

---

### 2. Frontend Setup (React + TypeScript Web)

```bash
# Navigate to frontend
cd ../frontend

# Install dependencies
npm install

# Start development web server
npm run dev

```

Open `http://localhost:5173` in your browser.

---

### 3. Running on Android (Capacitor)

```bash
cd frontend

# Build production TypeScript bundle
npm run build

# Add Android native platform (first time only)
npx cap add android

# Sync web build assets with native Android wrapper
npx cap sync android

# Open project in Android Studio to run on physical device or emulator
npx cap open android

```

---

## 📋 Development Roadmap

* [x] **Phase 1: Python Network Core**: Standalone ARP scanning with Scapy and async latency tracking with HTTPX.
* [x] **Phase 2: Real-time Backend Engine**: Integrate FastAPI, SQLite persistence, and Socket.IO broadcasts.
* [x] **Phase 3: React + TypeScript Web Dashboard**: Build mobile-friendly UI displaying connection health cards and device lists.
* [ ] **Phase 4: Mobile Compilation**: Configure Capacitor for Android, verify network permissions, and export build targets.
* [ ] **Phase 5: Push Notifications & Webhooks**: Add native push notifications for Android when unknown devices join the network.

---

## 🛡️ License

This project is open-source under the [MIT License](https://www.google.com/search?q=LICENSE).