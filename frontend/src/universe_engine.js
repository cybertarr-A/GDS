import * as THREE from "three";


class GDSUniverseEngine {

    constructor(scene) {
        this.scene = scene;
        this.starfield = null;
        this.nebulaSystem = null;
        this.galaxyRotationSpeed = 0.0003;
    }

    createCosmicEnvironment() {
        // 1. Multi-colored Starfield
        const starCount = 3000;
        const starGeo = new THREE.BufferGeometry();
        const positions = new Float32Array(starCount * 3);
        const colors = new Float32Array(starCount * 3);

        const colorOptions = [
            new THREE.Color(0x00f0ff),  // Cyan
            new THREE.Color(0xff00a0),  // Magenta
            new THREE.Color(0xb026ff),  // Purple
            new THREE.Color(0xffffff),  // Bright white
            new THREE.Color(0x5070a0)   // Deep blue
        ];

        for (let i = 0; i < starCount; i++) {
            // Position stars far in the background
            const radius = 60 + Math.random() * 80;
            const theta = Math.random() * Math.PI * 2;
            const phi = Math.acos((Math.random() * 2) - 1);

            positions[i * 3] = radius * Math.sin(phi) * Math.cos(theta);
            positions[i * 3 + 1] = radius * Math.sin(phi) * Math.sin(theta);
            positions[i * 3 + 2] = radius * Math.cos(phi);

            // Assign color
            const color = colorOptions[Math.floor(Math.random() * colorOptions.length)];
            colors[i * 3] = color.r;
            colors[i * 3 + 1] = color.g;
            colors[i * 3 + 2] = color.b;
        }

        starGeo.setAttribute("position", new THREE.BufferAttribute(positions, 3));
        starGeo.setAttribute("color", new THREE.BufferAttribute(colors, 3));

        const starMat = new THREE.PointsMaterial({
            size: 0.12,
            vertexColors: true,
            transparent: true,
            opacity: 0.8,
            blending: THREE.AdditiveBlending
        });

        this.starfield = new THREE.Points(starGeo, starMat);
        this.scene.add(this.starfield);

        // 2. Cosmic Nebula Dust particles
        const dustCount = 800;
        const dustGeo = new THREE.BufferGeometry();
        const dustPos = new Float32Array(dustCount * 3);
        const dustCols = new Float32Array(dustCount * 3);

        const nebulaColor = new THREE.Color(0x3e1882); // Dusty violet

        for (let i = 0; i < dustCount; i++) {
            // Clusters closer to the origin to simulate dust lanes
            const r = 5 + Math.random() * 30;
            const theta = Math.random() * Math.PI * 2;
            
            dustPos[i * 3] = r * Math.cos(theta) + (Math.random() - 0.5) * 6;
            dustPos[i * 3 + 1] = (Math.random() - 0.5) * 4;
            dustPos[i * 3 + 2] = r * Math.sin(theta) + (Math.random() - 0.5) * 6;

            dustCols[i * 3] = nebulaColor.r * (0.5 + Math.random() * 0.5);
            dustCols[i * 3 + 1] = nebulaColor.g * (0.5 + Math.random() * 0.5);
            dustCols[i * 3 + 2] = nebulaColor.b * (0.5 + Math.random() * 0.5);
        }

        dustGeo.setAttribute("position", new THREE.BufferAttribute(dustPos, 3));
        dustGeo.setAttribute("color", new THREE.BufferAttribute(dustCols, 3));

        const dustMat = new THREE.PointsMaterial({
            size: 0.4,
            vertexColors: true,
            transparent: true,
            opacity: 0.35,
            blending: THREE.AdditiveBlending,
            depthWrite: false
        });

        this.nebulaSystem = new THREE.Points(dustGeo, dustMat);
        this.scene.add(this.nebulaSystem);
    }

    animate() {
        if (this.starfield) {
            this.starfield.rotation.y += this.galaxyRotationSpeed;
            this.starfield.rotation.x += this.galaxyRotationSpeed * 0.2;
        }

        if (this.nebulaSystem) {
            this.nebulaSystem.rotation.y -= this.galaxyRotationSpeed * 0.5;
        }
    }
}

export default GDSUniverseEngine;
