import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
import GDSWebSocketClient from "./websocket_client.js";
import GDSUniverseBackground from "./universe_engine.js";
import GDSGraphRenderer from "./graph_renderer.js";
import GDSTemporalControls from "./temporal_controls.js";

// ==========================================
// 1. Initialize WebGL Context
// ==========================================

const container = document.getElementById("app-canvas-container");
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x020306); // Dark space void

const camera = new THREE.PerspectiveCamera(
    60,
    window.innerWidth / window.innerHeight,
    0.1,
    1000
);
camera.position.set(0, 0, 18);

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
container.appendChild(renderer.domElement);

// Orbital controls
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;
controls.maxDistance = 100;
controls.minDistance = 2;

// Lights
scene.add(new THREE.AmbientLight(0xffffff, 0.6));
const dirLight = new THREE.DirectionalLight(0xffffff, 1.2);
dirLight.position.set(10, 20, 15);
scene.add(dirLight);

// ==========================================
// 2. Initialize Visual Engines
// ==========================================

const cosmicBg = new GDSUniverseBackground(scene);
cosmicBg.createCosmicEnvironment();

const graphRenderer = new GDSGraphRenderer(scene, camera, renderer.domElement);

// Camera lerping target
let cameraFocusTarget = null;

// Filter state
let minEnergyFilter = 0.0;
let clusterFilter = "all";
let latestGraphData = null;

// ==========================================
// 3. WebSocket and Temporal Sync
// ==========================================

const wsClient = new GDSWebSocketClient();
const temporalControls = new GDSTemporalControls(wsClient);

// UI references
const sidebarDetailPlaceholder = document.querySelector(".details-placeholder");
const sidebarDetailContent = document.querySelector(".details-content");
const indicator = document.querySelector(".status-indicator");
const statusTxt = document.querySelector(".status-text");

// Handle stream packets
wsClient.connect((data) => {
    if (data.type === "connection_status") {
        if (data.connected) {
            indicator.className = "status-indicator online";
            statusTxt.textContent = "LIVING INTELLIGENCE ONLINE";
            temporalControls.updateTicker("Secure WebSocket uplink established.");
        } else {
            indicator.className = "status-indicator";
            statusTxt.textContent = "OFFLINE - RECONNECTING...";
            temporalControls.updateTicker("WebSocket disconnected. Retrying...");
        }
        return;
    }

    if (data.type === "initial_state" || data.type === "state_update" || data.type === "timeline_frame") {
        const graphData = data.type === "timeline_frame" ? data.snapshot : data;
        latestGraphData = graphData;

        // Render nodes and links
        graphRenderer.renderGraph(graphData, minEnergyFilter, clusterFilter);

        // Sync scrubber and play states
        if (data.playback) {
            temporalControls.syncState(data.playback, data.frame, data.timeline_size);
        }

        // Ticker update
        if (data.event) {
            temporalControls.updateTicker(data.event);
        }
    }

    if (data.type === "reasoning_result") {
        // Spawn simultaneous branching thought trails!
        if (data.branches && data.branches.length > 0) {
            graphRenderer.spawnBranchParticles(data.branches);
        }
        temporalControls.updateTicker(`Reasoning traversal completed. Confidence: ${Math.round(data.confidence * 100)}%`);
    }

    if (data.type === "prediction_result") {
        if (data.branches && data.branches.length > 0) {
            graphRenderer.drawPredictionBranches(data.branches);
        }
        temporalControls.updateTicker(`Predicted alternate futures calculated.`);
    }
});

// ==========================================
// 4. Register UI Actions & Hooks
// ==========================================

// Selected details metadata binding
graphRenderer.onHoverCallback = (nodeData) => {
    if (!nodeData && !graphRenderer.selectedNode) {
        sidebarDetailPlaceholder.style.display = "block";
        sidebarDetailContent.classList.add("hidden");
        return;
    }

    const node = nodeData || graphRenderer.selectedNode.userData;
    sidebarDetailPlaceholder.style.display = "none";
    sidebarDetailContent.classList.remove("hidden");

    document.getElementById("detail-id").textContent = node.id;
    document.getElementById("detail-content").textContent = node.content;
    document.getElementById("detail-energy").textContent = (node.energy || 0.5).toFixed(2);
    document.getElementById("detail-importance").textContent = (node.importance || 0.5).toFixed(2);
    document.getElementById("detail-attention").textContent = (node.attention || 0.05).toFixed(2);
    document.getElementById("detail-galaxy").textContent = `Galaxy ${node.cluster !== undefined ? node.cluster : '0'}`;
};

graphRenderer.onSelectCallback = (nodeData) => {
    graphRenderer.onHoverCallback(nodeData);
    
    // Zoom focus camera
    cameraFocusTarget = new THREE.Vector3(nodeData.x, nodeData.y, nodeData.z);
};

// Reasoning Trigger
document.getElementById("btn-reason").addEventListener("click", () => {
    if (graphRenderer.selectedNode) {
        const nodeId = graphRenderer.selectedNode.userData.id;
        wsClient.send("reason", { start_node: nodeId });
    }
});

// Alternate Future Prediction Trigger
document.getElementById("btn-predict").addEventListener("click", () => {
    if (graphRenderer.selectedNode) {
        const nodeId = graphRenderer.selectedNode.userData.id;
        wsClient.send("predict", { start_node: nodeId });
    }
});

// Filters re-renders
const energySlider = document.getElementById("filter-energy");
const energyVal = document.getElementById("energy-val");
energySlider.addEventListener("input", (e) => {
    minEnergyFilter = parseFloat(e.target.value);
    energyVal.textContent = minEnergyFilter.toFixed(1);
    if (latestGraphData) {
        graphRenderer.renderGraph(latestGraphData, minEnergyFilter, clusterFilter);
    }
});

const clusterSelect = document.getElementById("filter-cluster");
clusterSelect.addEventListener("change", (e) => {
    clusterFilter = e.target.value;
    if (latestGraphData) {
        graphRenderer.renderGraph(latestGraphData, minEnergyFilter, clusterFilter);
    }
});

// Thought Manual Injection
const injectInput = document.getElementById("inject-input");
const injectBtn = document.getElementById("inject-btn");
injectBtn.addEventListener("click", () => {
    const text = injectInput.value.trim();
    if (text) {
        wsClient.send("inject", { content: text });
        injectInput.value = "";
        temporalControls.updateTicker("Thought injection signal queued...");
    }
});

// Semantic Search
const searchInput = document.getElementById("search-input");
const searchBtn = document.getElementById("search-btn");
const searchResults = document.getElementById("search-results");

function executeSearch() {
    const query = searchInput.value.trim();
    if (!query) return;

    fetch(`http://127.0.0.1:8000/api/graph/search?q=${encodeURIComponent(query)}`)
        .then(res => res.json())
        .then(matches => {
            searchResults.innerHTML = "";
            if (matches.length === 0) {
                searchResults.innerHTML = '<div class="search-item">No matches discovered</div>';
                return;
            }

            matches.forEach(m => {
                const div = document.createElement("div");
                div.className = "search-item";
                div.textContent = `[Node ${m.id}] ${m.content}`;
                div.addEventListener("click", () => {
                    // Focus camera and select
                    const targetNode = graphRenderer.nodeMeshes.find(mesh => mesh.userData.id === m.id);
                    if (targetNode) {
                        graphRenderer.selectedNode = targetNode;
                        graphRenderer.onSelectCallback(targetNode.userData);
                    }
                });
                searchResults.appendChild(div);
            });
        });
}

searchBtn.addEventListener("click", executeSearch);
searchInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") executeSearch();
});

// ==========================================
// 5. Main Render Loop
// ==========================================

function animate() {
    requestAnimationFrame(animate);

    // Orbit controls update
    controls.update();

    // Background cosmic particle motion
    cosmicBg.animate();

    // Node glows, paths, branching thought lerps
    graphRenderer.animate();

    // Camera Focus Lerping zoom
    if (cameraFocusTarget) {
        const offset = new THREE.Vector3(0, 0, 5); // offsets camera looking in z-plane
        const targetCamPos = cameraFocusTarget.clone().add(offset);
        
        camera.position.lerp(targetCamPos, 0.05);
        controls.target.lerp(cameraFocusTarget, 0.05);

        if (camera.position.distanceTo(targetCamPos) < 0.05) {
            cameraFocusTarget = null; // zoom complete
        }
    }

    renderer.render(scene, camera);
}

// Window resizing
window.addEventListener("resize", () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

// Start loop
animate();