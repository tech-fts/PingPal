import type { LatencyPayload } from "../types";

interface Props {
  data: LatencyPayload | null;
}

const STATUS_COLORS: Record<string, string> = {
  green: "#22c55e",
  yellow: "#eab308",
  red: "#ef4444",
};

export default function NetworkStatus({ data }: Props) {
  const status = data?.status ?? "red";
  const latency = data?.latency ?? -1;

  return (
    <div className="network-status">
      <div className="status-indicator">
        <span
          className="status-dot"
          style={{ backgroundColor: STATUS_COLORS[status] }}
        />
        <span className="status-label">{status.toUpperCase()}</span>
      </div>
      <div className="latency-value">
        {latency >= 0 ? `${latency} ms` : "Offline"}
      </div>
    </div>
  );
}
