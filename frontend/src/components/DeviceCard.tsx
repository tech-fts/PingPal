import type { Device } from "../types";

interface Props {
  device: Device;
  isNew?: boolean;
}

export default function DeviceCard({ device, isNew = false }: Props) {
  return (
    <div className={`device-card${isNew ? " device-card--new" : ""}`}>
      <div className="device-card__header">
        <span className="device-card__name">{device.name ?? "Unknown Device"}</span>
        {isNew && <span className="device-card__badge">NEW</span>}
      </div>
      <div className="device-card__details">
        <div className="device-card__row">
          <span className="device-card__label">MAC</span>
          <code className="device-card__value">{device.mac}</code>
        </div>
        <div className="device-card__row">
          <span className="device-card__label">IP</span>
          <code className="device-card__value">{device.ip}</code>
        </div>
        {device.last_seen && (
          <div className="device-card__row">
            <span className="device-card__label">Last Seen</span>
            <span className="device-card__value">{device.last_seen}</span>
          </div>
        )}
      </div>
    </div>
  );
}
