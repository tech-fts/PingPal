import type { CapacitorConfig } from "@capacitor/cli";

const config: CapacitorConfig = {
  appId: "com.pingpal.app",
  appName: "PingPal",
  webDir: "dist",
  server: {
    androidScheme: "https",
  },
};

export default config;
