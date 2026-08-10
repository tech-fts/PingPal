import { useEffect, useState } from "react";
import { getSocket, disconnectSocket } from "./services/socket";
import NetworkStatus from "./components/NetworkStatus";
import DeviceCard from "./components/DeviceCard";
import LatencyChart from "./components/LatencyChart";
import type { LatencyPayload, Device, NewDevicePayload, DeviceListPayload } from "./types";
import "./index.css";

export default function App() {
  const [latency, setLatency] = useState<LatencyPayload | null>(null);
  const [history, setHistory] = useState<LatencyPayload[]>([]);
  const [devices, setDevices] = useState<Device[]>([]);
  const [newDevices, setNewDevices] = useState<Set<string>>(new Set());
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    const socket = getSocket();

    socket.on("connect", () => setConnected(true));
    socket.on("disconnect", () => setConnected(false));

    socket.on("latency_update", (data: LatencyPayload) => {
      setLatency(data);
      setHistory((prev) => [...prev.slice(-60), data]);
    });

    socket.on("new_device", (data: NewDevicePayload) => {
      setNewDevices((prev) => new Set(prev).add(data.mac));
    });

    socket.on("device_list_update", (data: DeviceListPayload) => {
      setDevices(data.devices);
    });

    return () => {
      disconnectSocket();
    };
  }, []);

  return (
    <div className="dashboard">
      <header className="dashboard__header">
        <h1>PingPal</h1>
        <div className={`connection-badge ${connected ? "connected" : "disconnected"}`}>
          {connected ? "Connected" : "Disconnected"}
        </div>
      </header>

      <main className="dashboard__grid">
        <section className="card status-card">
          <h2>Network Status</h2>
          <NetworkStatus data={latency} />
        </section>

        <section className="card chart-card">
          <h2>Latency History</h2>
          <LatencyChart history={history} />
        </section>

        <section className="card devices-card">
          <h2>
            Devices
            <span className="device-count">{devices.length}</span>
          </h2>
          {devices.length === 0 ? (
            <p className="empty-state">No devices discovered yet</p>
          ) : (
            <div className="device-list">
              {devices.map((d) => (
                <DeviceCard
                  key={d.mac}
                  device={d}
                  isNew={newDevices.has(d.mac)}
                />
              ))}
            </div>
          )}
        </section>
      </main>
    </div>
  );
}
