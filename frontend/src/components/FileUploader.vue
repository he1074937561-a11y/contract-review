<template>
  <div>
    <div
      style="border:2px dashed #d9d9d9;border-radius:16px;padding:48px;text-align:center;cursor:pointer;transition:all 0.3s;background:#fafafa;"
      :style="dragging ? 'border-color:#1e3a8a;background:#eff6ff;' : ''"
      @click="triggerUpload"
      @dragover.prevent="dragging = true"
      @dragleave="dragging = false"
      @drop.prevent="handleDrop"
    >
      <n-icon size="48" color="#1e3a8a">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
      </n-icon>
      <p style="font-size:16px;font-weight:600;margin-top:12px;">点击或将合同文件拖拽到此处</p>
      <p style="color:#999;font-size:13px;margin-top:4px;">支持 PDF, Word (docx), 图片 · 最大 50MB</p>
      <input ref="inputRef" type="file" accept=".pdf,.docx,.doc,.png,.jpg,.jpeg" style="display:none" @change="handleFileChange" />
    </div>
    <div v-if="selectedFile" style="margin-top:16px;padding:16px;background:#f9f9f9;border-radius:8px;display:flex;align-items:center;justify-content:space-between;">
      <div style="display:flex;align-items:center;gap:12px;">
        <n-icon size="32" color="#dc2626"><i class="fas fa-file-pdf"></i></n-icon>
        <div>
          <p style="font-weight:600;">{{ selectedFile.name }}</p>
          <p style="font-size:12px;color:#999;">{{ (selectedFile.size / 1024 / 1024).toFixed(1) }} MB · 准备就绪</p>
        </div>
      </div>
      <n-button quaternary circle size="small" @click="clearFile">
        <template #icon><n-icon><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg></n-icon></template>
      </n-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits<{ (e: 'file-selected', file: File | null): void }>()
const selectedFile = ref<File | null>(null)
const dragging = ref(false)
const inputRef = ref<HTMLInputElement>()

function triggerUpload() { inputRef.value?.click() }
function handleFileChange(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (file) { selectedFile.value = file; emit('file-selected', file) }
}
function handleDrop(e: DragEvent) {
  dragging.value = false
  const file = e.dataTransfer?.files?.[0]
  if (file) { selectedFile.value = file; emit('file-selected', file) }
}
function clearFile() { selectedFile.value = null; emit('file-selected', null) }
</script>
