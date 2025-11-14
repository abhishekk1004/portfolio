// three-landing.js
// Simple, efficient Three.js hero background scene
(function () {
  // wait until THREE is loaded
  if (typeof THREE === 'undefined') return console.warn('Three.js not loaded');

  // lazy init only when hero is visible
  let initialized = false;
  function initWhenVisible() {
    if (initialized) return;
    const wrap = document.getElementById('three-hero-wrap');
    if (!wrap) return;
    // only initialize when wrap is in DOM & visible
    const r = wrap.getBoundingClientRect();
    if (r.height === 0 && r.width === 0) return;
    initialized = true;
    initScene(wrap);
    // stop observing
    if (observer) observer.disconnect();
  }

  // use IntersectionObserver to lazy init
  let observer = null;
  if ('IntersectionObserver' in window) {
    observer = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (e.isIntersecting) initWhenVisible();
      });
    }, { root: null, threshold: 0.01 });
    const wrap = document.getElementById('three-hero-wrap');
    if (wrap) observer.observe(wrap);
  } else {
    // fallback: init after DOM load
    document.addEventListener('DOMContentLoaded', initWhenVisible);
    window.addEventListener('load', initWhenVisible);
  }

  function initScene(container) {
    // basic setup
    const scene = new THREE.Scene();
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.outputEncoding = THREE.sRGBEncoding;
    container.appendChild(renderer.domElement);

    // camera
    const camera = new THREE.PerspectiveCamera(50, container.clientWidth / container.clientHeight, 0.1, 1000);
    camera.position.set(0, 0, 4);

    // lights
    const hemi = new THREE.HemisphereLight(0xffffff, 0x444444, 0.7);
    scene.add(hemi);
    const dir = new THREE.DirectionalLight(0xffffff, 0.6);
    dir.position.set(5, 10, 7);
    scene.add(dir);

    // group for animation
    const group = new THREE.Group();
    scene.add(group);

    // create a cluster of low-poly shapes (fast)
    const material = new THREE.MeshStandardMaterial({
      color: 0xb774ff,
      metalness: 0.2,
      roughness: 0.35,
      emissive: 0x1a0b2a,
    });

    // add several toruses / icosahedrons
    const geom1 = new THREE.TorusGeometry(0.9, 0.18, 24, 64);
    const mesh1 = new THREE.Mesh(geom1, material);
    mesh1.position.set(-0.9, 0.25, 0);
    mesh1.rotation.set(0.4, 0.7, 0);
    group.add(mesh1);

    const geom2 = new THREE.IcosahedronGeometry(0.6, 1);
    const mat2 = material.clone(); mat2.color = new THREE.Color(0xffd36b);
    const mesh2 = new THREE.Mesh(geom2, mat2);
    mesh2.position.set(0.7, -0.15, -0.2);
    group.add(mesh2);

    const geom3 = new THREE.TorusKnotGeometry(0.45, 0.12, 120, 16);
    const mat3 = material.clone(); mat3.color = new THREE.Color(0x67e2ff);
    const mesh3 = new THREE.Mesh(geom3, mat3);
    mesh3.position.set(0.15, 0.7, -0.5);
    group.add(mesh3);

    // subtle environment / fog (optional)
    scene.fog = new THREE.FogExp2(0x000000, 0.05);

    // responsiveness
    function resize() {
      const w = container.clientWidth;
      const h = container.clientHeight;
      renderer.setSize(w, h);
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
    }
    window.addEventListener('resize', resize, { passive: true });

    // pause on tab hidden
    let isRunning = true;
    document.addEventListener('visibilitychange', () => {
      isRunning = document.visibilityState === 'visible';
    });

    // animation loop
    let t = 0;
    function animate() {
      if (isRunning) {
        t += 0.01;
        // rotate objects slowly
        group.rotation.y = Math.sin(t * 0.6) * 0.25;
        mesh1.rotation.x += 0.006;
        mesh1.rotation.y += 0.008;
        mesh2.rotation.x -= 0.01;
        mesh2.rotation.z += 0.007;
        mesh3.rotation.y -= 0.01;
        // gentle bob
        group.position.y = Math.sin(t * 0.8) * 0.06;
        renderer.render(scene, camera);
      }
      requestAnimationFrame(animate);
    }
    resize(); // initial size
    animate();

    // optional: load external glTF (3D logo) — uncomment & use if you have a model
    /*
    if (window.THREE && window.THREE.GLTFLoader) {
      const loader = new THREE.GLTFLoader();
      loader.load('/static/models/logo.glb', (gltf) => {
        const model = gltf.scene;
        model.scale.set(1.0,1.0,1.0);
        model.position.set(0,0,0);
        group.add(model);
      }, undefined, (err) => console.error('GLTF load error', err));
    }
    */
  }
})();
