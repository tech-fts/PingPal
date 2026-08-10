// === PingPal TypeScript Interfaces ===

export interface LatencyPayload {
  latency: number;
  status: "green" | "yellow" | "red";
}

export interface Device {
  mac: string;
  ip: string;
  name?: string;
  first_seen?: string;
  last_seen?: string;
}

export interface NewDevicePayload {
  mac: string;
  ip: string;
}

export interface DeviceListPayload {
  devices: Device[];
}

// Socket.io event map — server → client
export interface ServerToClientEvents {
  latency_update: (data: LatencyPayload) => void;
  new_device: (data: NewDevicePayload) => void;
  device_list_update: (data: DeviceListPayload) => void;
}

// Socket.io event map — client → server (reserved for future use)
export interface ClientToServerEvents {}
