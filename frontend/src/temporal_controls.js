class GDSTemporalControls {

    constructor(wsClient) {
        this.ws = wsClient;

        // Cache DOM elements
        this.btnPlay = document.getElementById("btn-play");
        this.btnPause = document.getElementById("btn-pause");
        this.btnReverse = document.getElementById("btn-reverse");
        this.speedSelector = document.getElementById("playback-speed");
        this.scrubber = document.getElementById("timeline-scrubber");
        this.frameCounter = document.getElementById("frame-num");
        this.totalFramesCounter = document.getElementById("total-frames");
        this.ticker = document.getElementById("ticker-text");

        this.isScrubbing = false;

        this.initEvents();
    }

    initEvents() {
        // Play
        this.btnPlay.addEventListener("click", () => {
            this.ws.send("timeline_play");
            this.setPlayState(true);
        });

        // Pause
        this.btnPause.addEventListener("click", () => {
            this.ws.send("timeline_pause");
            this.setPlayState(false);
        });

        // Reverse
        this.btnReverse.addEventListener("click", () => {
            fetch("http://127.0.0.1:8000/timeline/reverse", { method: "POST" })
                .then(r => r.json())
                .then(data => {
                    this.updateTicker(`Simulation direction reversed: ${data.direction === 1 ? 'Forward' : 'Backward'}`);
                });
        });

        // Speed warp selector
        this.speedSelector.addEventListener("change", (e) => {
            const speed = parseFloat(e.target.value);
            fetch("http://127.0.0.1:8000/timeline/speed", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ speed })
            })
            .then(r => r.json())
            .then(data => {
                this.updateTicker(`Time warp speed adjusted: ${data.speed}x`);
            });
        });

        // Scrubber sliding
        this.scrubber.addEventListener("input", (e) => {
            this.isScrubbing = true;
            const frame = parseInt(e.target.value);
            this.frameCounter.textContent = frame;
            
            // Scrub using websocket
            this.ws.send("timeline_scrub", { frame });
        });

        this.scrubber.addEventListener("change", () => {
            this.isScrubbing = false;
        });
    }

    setPlayState(isPlaying) {
        if (isPlaying) {
            this.btnPlay.classList.add("active");
            this.btnPause.classList.remove("active");
        } else {
            this.btnPlay.classList.remove("active");
            this.btnPause.classList.add("active");
        }
    }

    syncState(playback, frame, timelineSize) {
        // Sync play/pause buttons
        this.setPlayState(playback.is_playing);

        // Sync speed drop-down
        this.speedSelector.value = String(playback.speed);

        // Sync timeline scrubber limits & values
        if (!this.isScrubbing) {
            this.scrubber.max = Math.max(0, timelineSize - 1);
            this.scrubber.value = frame;
            
            this.frameCounter.textContent = frame;
            this.totalFramesCounter.textContent = Math.max(0, timelineSize - 1);
        }
    }

    updateTicker(message) {
        if (this.ticker) {
            this.ticker.textContent = message;
            // Sleek text flash animation on update
            this.ticker.style.color = "#00f0ff";
            setTimeout(() => {
                this.ticker.style.color = "#8e9bb4";
            }, 1000);
        }
    }
}

export default GDSTemporalControls;
