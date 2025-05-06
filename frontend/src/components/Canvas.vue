<template>
    <div class="">
    <div v-if="loading" class="loading-overlay">
      <h2>Yükleniyor...</h2>
    </div>
    <div v-else
         class="canvas-row"
        v-for="(row, y) in canvas"
        :key="y"
        style="display: flex"
      >
        <div
        class="canvas-cell"
          v-for="(color, x) in row"
          :key="x"
          :style="{
            width: '12px',
            height: '12px',
            background: color,
            cursor: 'pointer'
          }"
          @click="openModal(x, y)"
        ></div>
      </div>
  
      <!-- Modal -->
      <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
        <div class="modal">
          <h3>Renk Seç</h3>
          <div style="display: flex; flex-wrap: wrap; gap: 8px;">
            <div
              v-for="color in colors"
              :key="color"
              :style="{
                width: '32px',
                height: '32px',
                background: color,
                cursor: 'pointer',
                border: '1px solid #ccc'
              }"
              @click="selectColor(color)"
            ></div>
          </div>
          <button @click="closeModal" style="margin-top: 16px;">Vazgeç</button>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  const canvas = ref([])
  const showModal = ref(false)
  const selectedX = ref(0)
  const selectedY = ref(0)
  const colors = [
        "#6d001a",
        "#be0039",
        "#ff4500",
        "#ffa800",
        "#ffd635",
        "#fff8b8",
        "#00a368",
        "#00cc78",
        "#7eed56",
        "#00756f",
        "#009eaa",
        "#00ccc0",
        "#2450a4",
        "#3690ea",
        "#51e9f4",
        "#493ac1",
        "#6a5cff",
        "#94b3ff",
        "#811e9f",
        "#b44ac0",
        "#e4abff",
        "#de107f",
        "#ff3881",
        "#ff99aa",
        "#6d482f",
        "#9c6926",
        "#ffb470",
        "#000000",
        "#515252",
        "#898d90",
        "#d4d7d9",
        "#ffffff",
  ]
  const loading = ref(true)
  const pre_loading = ref(false)

  async function fetchCanvas() {
    loading.value = true
    const res = await fetch('http://localhost:8000/canvas')
    const data = await res.json()
    canvas.value = data.canvas
    loading.value = false


  }
  
  function openModal(x, y) {
    selectedX.value = x
    selectedY.value = y
    showModal.value = true
  }
  
  function closeModal() {
    showModal.value = false
  }
  
  async function selectColor(color) {

    await fetch('http://localhost:8000/pixel', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ x: selectedX.value, y: selectedY.value, color })
    })
    showModal.value = false
  }
  onMounted(() => {
  fetchCanvas()
  const ws = new WebSocket('ws://localhost:8000/ws')
  ws.onopen = () => {
    loading.value = false
  }
  ws.onmessage = (event) => {
    if (!pre_loading.value){
        console.log('İlk giriş tamam')
        loading.value = false
        pre_loading.value = true
    }
    const data = JSON.parse(event.data)
    canvas.value[data.y][data.x] = data.color
  }
  ws.onclose = () => {
    loading.value = true
  }
})
  </script>
  
  <style scoped>
  .canvas-wrapper {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f7f7f7;
}
.canvas {
  display: inline-block;
  box-shadow: 0 2px 16px rgba(0,0,0,0.08);
  border-radius: 8px;
  padding: 8px;
  background: #fff;
}
.canvas-row {
  border: '1px solid #ccc';
  display: flex;
}
.canvas-cell {
  width: 16px;
  height: 16px;
  cursor: pointer;
  transition: box-shadow 0.1s;
}
.canvas-cell:hover {
  box-shadow: 0 0 4px #888;
  z-index: 1;
  border: 1px solid #ccc;
}
  .loading-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(255,255,255,0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  z-index: 2000;
}
  .modal-overlay {
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(0,0,0,0.4);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
  }
  .modal {
    background: #fff;
    padding: 24px;
    border-radius: 8px;
    min-width: 240px;
    box-shadow: 0 2px 16px rgba(0,0,0,0.2);
  }
  </style>

