// app.js
let scene, camera, renderer, hologram;

function initHologram() {
  const canvas = document.getElementById('hologram');
  canvas.style.position = 'absolute';
  canvas.style.top = '0';
  canvas.style.left = '0';
  canvas.style.width = '100%';
  canvas.style.height = '100%';
  canvas.style.zIndex = '-1';
  
  scene = new THREE.Scene();
  camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
  renderer = new THREE.WebGLRenderer({ canvas, alpha: true });
  renderer.setSize(window.innerWidth, window.innerHeight);
  

  const geometry = new THREE.IcosahedronGeometry(10);
  const material = new THREE.MeshBasicMaterial({ 
    color: 0x00fffc,
    wireframe: true,
    transparent: true,
    opacity: 0.3
  });
  hologram = new THREE.Mesh(geometry, material);
  scene.add(hologram);
  
  camera.position.z = 30;
  
  animate();
}

function animate() {
  requestAnimationFrame(animate);
  hologram.rotation.x += 0.01;
  hologram.rotation.y += 0.01;
  renderer.render(scene, camera);
}

async function fetchSystemData() {
  try {
    const response = await fetch('http://localhost:5000/system_info');
    const data = await response.json();
    
  
    document.getElementById('cpu-usage').innerHTML = `Usage: ${data.cpu.usage}%`;
    document.getElementById('cpu-cores').innerHTML = `Cores: ${data.cpu.cores} (${data.cpu.threads} threads)`;
    
    document.getElementById('memory-usage').innerHTML = 
      `Used: ${(data.memory.used / (1024 ** 3)).toFixed(2)}GB (${data.memory.percent}%)`;
    document.getElementById('memory-available').innerHTML = 
      `Available: ${(data.memory.available / (1024 ** 3)).toFixed(2)}GB`;
    
  } catch (error) {
    console.error('Error fetching system data:', error);
  }
}

window.onload = function() {
  initHologram();
  fetchSystemData();
  setInterval(fetchSystemData, 2000)
};