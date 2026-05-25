import * as THREE from "three";

class GDSGraphRenderer {

    constructor(scene, camera, domElement) {
        this.scene = scene;
        this.camera = camera;
        this.domElement = domElement;

        this.nodeMeshes = [];
        this.nodeMap = {};
        this.edges = [];
        
        // Beam/Reasoning particles
        this.thoughtParticles = [];
        this.branchParticles = [];

        // Attention waves
        this.attentionWaves = [];

        // Interactive states
        this.raycaster = new THREE.Raycaster();
        this.mouse = new THREE.Vector2();
        this.hoveredNode = null;
        this.selectedNode = null;

        // Callback hooks
        this.onHoverCallback = null;
        this.onSelectCallback = null;

        // Initialize raycasting events
        this.domElement.addEventListener("mousemove", (e) => this.onMouseMove(e));
        this.domElement.addEventListener("click", (e) => this.onClick(e));
    }

    clearGraph() {
        this.nodeMeshes.forEach(m => this.scene.remove(m));
        this.edges.forEach(e => this.scene.remove(e.line));
        this.thoughtParticles.forEach(p => this.scene.remove(p.mesh));
        this.branchParticles.forEach(p => this.scene.remove(p.mesh));
        this.attentionWaves.forEach(w => this.scene.remove(w.mesh));

        this.nodeMeshes = [];
        this.nodeMap = {};
        this.edges = [];
        this.thoughtParticles = [];
        this.branchParticles = [];
        this.attentionWaves = [];
    }

    renderGraph(data, filterMinEnergy = 0.0, filterCluster = "all") {
        this.clearGraph();

        if (!data || !data.nodes) return;

        // 1. Create Clustered Nodes
        data.nodes.forEach((node, index) => {
            const energy = node.energy !== undefined ? node.energy : 0.5;
            const cluster = node.cluster !== undefined ? node.cluster : 0;

            // Apply filters
            if (energy < filterMinEnergy) return;
            if (filterCluster !== "all" && String(cluster) !== String(filterCluster)) return;

            // Positioning: use backend values or circular default fallback
            let x = node.x !== undefined ? node.x : Math.cos((index / data.nodes.length) * Math.PI * 2) * 5;
            let y = node.y !== undefined ? node.y : Math.sin((index / data.nodes.length) * Math.PI * 2) * 5;
            let z = node.z !== undefined ? node.z : (Math.random() - 0.5) * 2;

            // Hue based on energy: Blue -> Magenta -> Gold -> Orange-Red
            const hue = 220 - (energy * 200);
            
            const mat = new THREE.MeshStandardMaterial({
                color: new THREE.Color().setHSL(hue / 360, 0.9, 0.5),
                emissive: new THREE.Color().setHSL(hue / 360, 0.9, 0.5),
                emissiveIntensity: energy * 2.0,
                roughness: 0.1,
                metalness: 0.1
            });

            const geom = new THREE.SphereGeometry((node.importance || 0.5) * 0.35 + 0.1, 32, 32);
            const sphere = new THREE.Mesh(geom, mat);
            sphere.position.set(x, y, z);
            sphere.userData = node;

            // Sleek glowing shell ring representing attention
            const ringGeom = new THREE.RingGeometry(((node.importance || 0.5) * 0.35 + 0.15), ((node.importance || 0.5) * 0.35 + 0.18), 32);
            const ringMat = new THREE.MeshBasicMaterial({
                color: 0x00f0ff,
                transparent: true,
                opacity: 0.0,
                side: THREE.DoubleSide
            });
            const ring = new THREE.Mesh(ringGeom, ringMat);
            sphere.add(ring);
            sphere.userData.attentionRing = ring;

            this.scene.add(sphere);
            this.nodeMeshes.push(sphere);
            this.nodeMap[node.id] = sphere;
        });

        // 2. Create Curved/Glow Edges
        data.edges.forEach(edge => {
            const source = this.nodeMap[edge.source];
            const target = this.nodeMap[edge.target];

            if (!source || !target) return;

            // Sleek straight lines
            const geom = new THREE.BufferGeometry().setFromPoints([
                source.position,
                target.position
            ]);

            const lineMat = new THREE.LineBasicMaterial({
                color: 0x00f0ff,
                transparent: true,
                opacity: 0.25 + (edge.weight || 0.5) * 0.4,
                blending: THREE.AdditiveBlending
            });

            const line = new THREE.Line(geom, lineMat);
            this.scene.add(line);

            this.edges.push({
                sourceId: edge.source,
                targetId: edge.target,
                line: line,
                sourcePos: source.position,
                targetPos: target.position,
                weight: edge.weight || 0.5
            });
        });

        // 3. Trigger Thought Particle walks if reasoning path is active
        if (data.reasoning_path && data.reasoning_path.length > 1) {
            this.startThoughtTraversal(data.reasoning_path, data.confidence || 0.8);
        }
    }

    startThoughtTraversal(path, confidence = 0.8) {
        // Main traversal particle
        const particleMat = new THREE.MeshBasicMaterial({
            color: 0xff00a0,
            transparent: true,
            opacity: 1.0,
            blending: THREE.AdditiveBlending
        });

        const pGeom = new THREE.SphereGeometry(0.12, 16, 16);
        const pMesh = new THREE.Mesh(pGeom, particleMat);
        
        // Spawn first node
        const firstNode = this.nodeMap[path[0]];
        if (firstNode) {
            pMesh.position.copy(firstNode.position);
            this.scene.add(pMesh);
            
            // Particle state: speed is confidence weighted
            this.thoughtParticles.push({
                mesh: pMesh,
                path: path,
                currIndex: 0,
                progress: 0.0,
                speed: 0.01 + confidence * 0.018
            });
        }
    }

    spawnBranchParticles(branches) {
        if (!branches || branches.length === 0) return;

        branches.forEach(branch => {
            const startNode = this.nodeMap[branch.split_node];
            if (!startNode) return;

            const particleMat = new THREE.MeshBasicMaterial({
                color: 0xffe600, // Gold for branches
                transparent: true,
                opacity: 0.9,
                blending: THREE.AdditiveBlending
            });
            const pMesh = new THREE.Mesh(new THREE.SphereGeometry(0.09, 16, 16), particleMat);
            pMesh.position.copy(startNode.position);
            this.scene.add(pMesh);

            this.branchParticles.push({
                mesh: pMesh,
                path: [branch.split_node, ...branch.path.map(p => p.id)],
                currIndex: 0,
                progress: 0.0,
                speed: 0.012 + branch.confidence * 0.01
            });
        });
    }

    triggerAttentionWave(nodeId) {
        const node = this.nodeMap[nodeId];
        if (!node) return;

        const waveMat = new THREE.MeshBasicMaterial({
            color: 0x00f0ff,
            transparent: true,
            opacity: 0.8,
            side: THREE.DoubleSide
        });

        const waveMesh = new THREE.Mesh(new THREE.RingGeometry(0.1, 0.2, 32), waveMat);
        waveMesh.position.copy(node.position);
        
        // Lock rotation facing camera
        waveMesh.quaternion.copy(this.camera.quaternion);

        this.scene.add(waveMesh);
        this.attentionWaves.push({
            mesh: waveMesh,
            radius: 0.2,
            maxRadius: 3.5,
            opacity: 0.8
        });
    }

    onMouseMove(event) {
        // Calculate mouse position in normalized device coordinates
        const rect = this.domElement.getBoundingClientRect();
        this.mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
        this.mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
    }

    onClick() {
        if (this.hoveredNode) {
            this.selectedNode = this.hoveredNode;
            if (this.onSelectCallback) {
                this.onSelectCallback(this.selectedNode.userData);
            }
            
            // Visual pulse on selection
            this.triggerAttentionWave(this.selectedNode.userData.id);
        }
    }

    animate() {
        // 1. Raycast hover check
        this.raycaster.setFromCamera(this.mouse, this.camera);
        const intersects = this.raycaster.intersectObjects(this.nodeMeshes);

        if (intersects.length > 0) {
            const target = intersects[0].object;
            if (this.hoveredNode !== target) {
                this.hoveredNode = target;
                if (this.onHoverCallback) {
                    this.onHoverCallback(target.userData);
                }
            }
        } else {
            if (this.hoveredNode !== null) {
                this.hoveredNode = null;
                if (this.onHoverCallback) {
                    this.onHoverCallback(null);
                }
            }
        }

        // 2. Animate nodes (glow pulses and rotations)
        const time = Date.now() * 0.002;
        this.nodeMeshes.forEach(mesh => {
            const energy = mesh.userData.energy || 0.5;
            const attention = mesh.userData.attention || 0.05;
            const pulse = Math.sin(time + mesh.userData.id) * 0.3 + 0.7;

            // Core glow intensity
            mesh.material.emissiveIntensity = energy * 1.5 + attention * 4.0 + pulse * 0.5;

            // Scale adjustment based on attention spike
            const scaleBase = 1.0 + attention * 0.3;
            mesh.scale.set(scaleBase, scaleBase, scaleBase);

            // Animate attention rings
            if (mesh.userData.attentionRing) {
                const ring = mesh.userData.attentionRing;
                ring.quaternion.copy(this.camera.quaternion); // Face camera
                
                if (attention > 0.05) {
                    ring.material.opacity = attention * 0.8;
                    const ringScale = 1.0 + Math.sin(time * 3 + mesh.userData.id) * 0.15;
                    ring.scale.set(ringScale, ringScale, 1.0);
                } else {
                    ring.material.opacity = 0.0;
                }
            }
        });

        // 3. Animate Thought Particles
        this.thoughtParticles.forEach((p, idx) => {
            if (p.path.length < 2) return;

            const sourceNode = this.nodeMap[p.path[p.currIndex]];
            const targetNode = this.nodeMap[p.path[(p.currIndex + 1) % p.path.length]];

            if (sourceNode && targetNode) {
                p.mesh.position.lerpVectors(
                    sourceNode.position,
                    targetNode.position,
                    p.progress
                );

                p.progress += p.speed;

                if (p.progress >= 1.0) {
                    p.progress = 0.0;
                    p.currIndex = (p.currIndex + 1) % (p.path.length - 1);
                    
                    // Trigger dynamic pulse when passing a node
                    const nextId = p.path[p.currIndex];
                    this.triggerAttentionWave(nextId);
                }
            }
        });

        // 4. Animate Branching Particles
        const finishedBranches = [];
        this.branchParticles.forEach((bp, idx) => {
            if (bp.path.length < 2) return;

            const sourceNode = this.nodeMap[bp.path[bp.currIndex]];
            const targetNode = this.nodeMap[bp.path[bp.currIndex + 1]];

            if (sourceNode && targetNode) {
                bp.mesh.position.lerpVectors(
                    sourceNode.position,
                    targetNode.position,
                    bp.progress
                );

                bp.progress += bp.speed;

                if (bp.progress >= 1.0) {
                    bp.progress = 0.0;
                    bp.currIndex++;

                    if (bp.currIndex >= bp.path.length - 1) {
                        // End of branch trail
                        finishedBranches.push(idx);
                        this.scene.remove(bp.mesh);
                    }
                }
            } else {
                finishedBranches.push(idx);
                this.scene.remove(bp.mesh);
            }
        });

        // Remove finished branches
        finishedBranches.reverse().forEach(idx => {
            this.branchParticles.splice(idx, 1);
        });

        // 5. Animate Attention Waves
        const finishedWaves = [];
        this.attentionWaves.forEach((w, idx) => {
            w.radius += 0.06;
            w.opacity -= 0.02;

            if (w.opacity <= 0.0 || w.radius >= w.maxRadius) {
                finishedWaves.push(idx);
                this.scene.remove(w.mesh);
            } else {
                // Update ring geometry
                this.scene.remove(w.mesh);
                
                const g = new THREE.RingGeometry(w.radius - 0.1, w.radius, 32);
                const m = new THREE.MeshBasicMaterial({
                    color: 0x00f0ff,
                    transparent: true,
                    opacity: w.opacity,
                    side: THREE.DoubleSide,
                    blending: THREE.AdditiveBlending
                });
                
                const newMesh = new THREE.Mesh(g, m);
                newMesh.position.copy(w.mesh.position);
                newMesh.quaternion.copy(this.camera.quaternion);
                
                this.scene.add(newMesh);
                w.mesh = newMesh;
            }
        });

        // Remove finished waves
        finishedWaves.reverse().forEach(idx => {
            this.attentionWaves.splice(idx, 1);
        });
    }
}

export default GDSGraphRenderer;
