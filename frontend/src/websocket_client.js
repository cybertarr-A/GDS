class GDSWebSocketClient {

    constructor(url = null) {
        this.url = url || `ws://${window.location.hostname || '127.0.0.1'}:8000/api/ws`;
        this.socket = null;
        this.listeners = [];
        this.reconnectTimer = null;
        this.isConnected = false;
    }

    connect(onStateUpdate = null) {
        if (onStateUpdate) {
            this.addListener(onStateUpdate);
        }

        console.log(`[INFO] Attempting WebSocket connection to: ${this.url}`);
        
        try {
            this.socket = new WebSocket(this.url);

            this.socket.onopen = () => {
                console.log("[INFO] Connected to GDS WebSocket backend.");
                this.isConnected = true;
                if (this.reconnectTimer) {
                    clearTimeout(this.reconnectTimer);
                    this.reconnectTimer = null;
                }
                
                // Dispatch connection state
                this.triggerListeners({ type: "connection_status", connected: true });
            };

            this.socket.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    this.triggerListeners(data);
                } catch (e) {
                    console.error("[ERROR] Failed to parse WebSocket packet:", e);
                }
            };

            this.socket.onclose = () => {
                console.warn("[WARNING] GDS WebSocket closed. Attempting reconnect...");
                this.isConnected = false;
                this.triggerListeners({ type: "connection_status", connected: false });
                this.scheduleReconnect();
            };

            this.socket.onerror = (err) => {
                console.error("[ERROR] WebSocket connection error:", err);
                this.socket.close();
            };

        } catch (e) {
            console.error("[ERROR] Failed to instantiate WebSocket:", e);
            this.scheduleReconnect();
        }
    }

    scheduleReconnect() {
        if (this.reconnectTimer) return;
        this.reconnectTimer = setTimeout(() => {
            this.reconnectTimer = null;
            this.connect();
        }, 3000); // retry every 3s
    }

    addListener(callback) {
        this.listeners.push(callback);
    }

    triggerListeners(data) {
        this.listeners.forEach(cb => cb(data));
    }

    send(action, payload = {}) {
        if (!this.isConnected || !this.socket) {
            console.error("[ERROR] Cannot send payload, WebSocket not connected.");
            return false;
        }

        const msg = JSON.stringify({ action, ...payload });
        this.socket.send(msg);
        return true;
    }
}

export default GDSWebSocketClient;
