import * as THREE from "three";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";

const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const canvas = document.getElementById("space-canvas");
if (!canvas) throw new Error("space canvas missing");

const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.75));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.outputColorSpace = THREE.SRGBColorSpace;

const scene = new THREE.Scene();
scene.fog = new THREE.FogExp2(0x06140c, 0.028);

const camera = new THREE.PerspectiveCamera(42, window.innerWidth / window.innerHeight, 0.1, 80);
camera.position.set(0, 0.35, 6.2);

scene.add(new THREE.AmbientLight(0x7cff9a, 0.35));
const key = new THREE.DirectionalLight(0xffffff, 1.15);
key.position.set(3, 4, 5);
scene.add(key);
const rim = new THREE.DirectionalLight(0x3dff7a, 0.7);
rim.position.set(-4, 1, -3);
scene.add(rim);
const fill = new THREE.PointLight(0x86ffc1, 8, 18);
fill.position.set(0, -1.4, 2);
scene.add(fill);

const hero = new THREE.Group();
scene.add(hero);

const debris = new THREE.Group();
scene.add(debris);

function makeNail() {
  const group = new THREE.Group();
  const metal = new THREE.MeshStandardMaterial({
    color: 0xb7c4bb,
    metalness: 0.82,
    roughness: 0.32,
  });
  const rust = new THREE.MeshStandardMaterial({
    color: 0x6d7a63,
    metalness: 0.55,
    roughness: 0.55,
  });
  const shaft = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.02, 0.55, 6), metal);
  const head = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 0.045, 8), rust);
  head.position.y = 0.28;
  group.add(shaft, head);
  return group;
}

function makeScrap() {
  const kind = Math.floor(Math.random() * 4);
  const mat = new THREE.MeshStandardMaterial({
    color: new THREE.Color().setHSL(0.33, 0.25, 0.45 + Math.random() * 0.2),
    metalness: 0.7,
    roughness: 0.4,
  });
  if (kind === 0) return new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.06, 0.16), mat);
  if (kind === 1) return new THREE.Mesh(new THREE.TorusGeometry(0.09, 0.025, 8, 14), mat);
  if (kind === 2) return new THREE.Mesh(new THREE.OctahedronGeometry(0.12), mat);
  return new THREE.Mesh(new THREE.ConeGeometry(0.06, 0.28, 5), mat);
}

const floaters = [];
for (let i = 0; i < 70; i += 1) {
  const item = i % 2 === 0 ? makeNail() : makeScrap();
  const radius = 3.2 + Math.random() * 7;
  const theta = Math.random() * Math.PI * 2;
  const phi = Math.acos(2 * Math.random() - 1);
  item.position.set(
    radius * Math.sin(phi) * Math.cos(theta),
    radius * Math.cos(phi) * 0.7,
    radius * Math.sin(phi) * Math.sin(theta) - 1.5
  );
  item.rotation.set(Math.random() * 6, Math.random() * 6, Math.random() * 6);
  item.scale.setScalar(0.55 + Math.random() * 1.1);
  debris.add(item);
  floaters.push({
    mesh: item,
    spin: new THREE.Vector3(
      (Math.random() - 0.5) * 0.35,
      (Math.random() - 0.5) * 0.55,
      (Math.random() - 0.5) * 0.35
    ),
  });
}

const starGeo = new THREE.BufferGeometry();
const starCount = 420;
const starPos = new Float32Array(starCount * 3);
for (let i = 0; i < starCount; i += 1) {
  starPos[i * 3] = (Math.random() - 0.5) * 40;
  starPos[i * 3 + 1] = (Math.random() - 0.5) * 28;
  starPos[i * 3 + 2] = (Math.random() - 0.5) * 40 - 6;
}
starGeo.setAttribute("position", new THREE.BufferAttribute(starPos, 3));
scene.add(new THREE.Points(
  starGeo,
  new THREE.PointsMaterial({ color: 0xc8ffd8, size: 0.035, transparent: true, opacity: 0.75 })
));

const loader = new GLTFLoader();
loader.load(
  "/static/hero.glb",
  (gltf) => {
    const model = gltf.scene;
    model.traverse((node) => {
      if (node.isMesh) {
        node.castShadow = false;
        node.receiveShadow = false;
        if (node.material) {
          node.material.envMapIntensity = 0.8;
        }
      }
    });
    const box = new THREE.Box3().setFromObject(model);
    const size = box.getSize(new THREE.Vector3());
    const center = box.getCenter(new THREE.Vector3());
    model.position.sub(center);
    const scale = 2.6 / Math.max(size.x, size.y, size.z);
    model.scale.setScalar(scale);
    hero.add(model);
    document.body.classList.add("space-on");
  },
  undefined,
  () => {
    document.body.classList.add("space-on");
  }
);

function onResize() {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
}
window.addEventListener("resize", onResize);

let last = performance.now();
function tick(now) {
  const dt = Math.min((now - last) / 1000, 0.05);
  last = now;
  if (!reduced) {
    hero.rotation.y += dt * 0.12;
    hero.position.y = Math.sin(now * 0.00045) * 0.12;
    debris.rotation.y += dt * 0.02;
    floaters.forEach((item) => {
      item.mesh.rotation.x += item.spin.x * dt;
      item.mesh.rotation.y += item.spin.y * dt;
      item.mesh.rotation.z += item.spin.z * dt;
    });
  }
  renderer.render(scene, camera);
  requestAnimationFrame(tick);
}
requestAnimationFrame(tick);
