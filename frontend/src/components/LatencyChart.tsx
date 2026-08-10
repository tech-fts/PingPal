import { useEffect, useRef } from "react";
import type { LatencyPayload } from "../types";

interface Props {
  history: LatencyPayload[];
  maxPoints?: number;
}

export default function LatencyChart({ history, maxPoints = 30 }: Props) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const dpr = window.devicePixelRatio || 1;
    const rect = canvas.getBoundingClientRect();
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    ctx.scale(dpr, dpr);

    const w = rect.width;
    const h = rect.height;
    const pad = { top: 10, right: 10, bottom: 20, left: 50 };
    const plotW = w - pad.left - pad.right;
    const plotH = h - pad.top - pad.bottom;

    // Clear
    ctx.clearRect(0, 0, w, h);

    if (history.length < 2) {
      ctx.fillStyle = "#6b7280";
      ctx.font = "14px system-ui";
      ctx.textAlign = "center";
      ctx.fillText("Waiting for data...", w / 2, h / 2);
      return;
    }

    const points = history.slice(-maxPoints);
    const maxLatency = Math.max(...points.map((p) => p.latency), 300);
    const minLatency = 0;

    const scaleX = (i: number) => pad.left + (i / (points.length - 1)) * plotW;
    const scaleY = (v: number) =>
      pad.top + plotH - ((v - minLatency) / (maxLatency - minLatency)) * plotH;

    // Grid lines
    ctx.strokeStyle = "#374151";
    ctx.lineWidth = 0.5;
    for (let i = 0; i <= 4; i++) {
      const y = pad.top + (plotH / 4) * i;
      ctx.beginPath();
      ctx.moveTo(pad.left, y);
      ctx.lineTo(pad.left + plotW, y);
      ctx.stroke();

      const label = Math.round(maxLatency - (maxLatency / 4) * i);
      ctx.fillStyle = "#6b7280";
      ctx.font = "10px system-ui";
      ctx.textAlign = "right";
      ctx.fillText(`${label}`, pad.left - 6, y + 4);
    }

    // Latency line
    ctx.beginPath();
    ctx.strokeStyle = "#c084fc";
    ctx.lineWidth = 2;
    ctx.lineJoin = "round";

    points.forEach((p, i) => {
      const x = scaleX(i);
      const y = scaleY(Math.max(p.latency, 0));
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    });
    ctx.stroke();

    // Status dots
    points.forEach((p, i) => {
      const x = scaleX(i);
      const y = scaleY(Math.max(p.latency, 0));
      ctx.beginPath();
      ctx.arc(x, y, 3, 0, Math.PI * 2);
      ctx.fillStyle =
        p.status === "green" ? "#22c55e" : p.status === "yellow" ? "#eab308" : "#ef4444";
      ctx.fill();
    });
  }, [history, maxPoints]);

  return (
    <div className="latency-chart">
      <canvas ref={canvasRef} className="latency-chart__canvas" />
    </div>
  );
}
