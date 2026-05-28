<template>
  <div style="max-width:600px;margin:80px auto;text-align:center;">
    <!-- Working -->
    <div v-if="stage === 'working'" style="background:#fff;border-radius:12px;padding:48px;border:1px solid #e0e7ff;">
      <svg viewBox="0 0 80 80" style="width:80px;height:80px;">
        <defs>
          <linearGradient id="sg" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#4f46e5"/>
            <stop offset="100%" stop-color="#818cf8"/>
          </linearGradient>
        </defs>
        <circle cx="40" cy="40" r="32" fill="none" stroke="#e0e7ff" stroke-width="6"/>
        <path d="M40 8 A32 32 0 0 1 72 40" fill="none" stroke="url(#sg)" stroke-width="6" stroke-linecap="round">
          <animateTransform attributeName="transform" type="rotate" from="0 40 40" to="360 40 40" dur="1.2s" repeatCount="indefinite"/>
        </path>
      </svg>
      <h2 style="font-size:18px;margin:20px 0 8px;">正在分析合同</h2>
      <p style="color:#999;font-size:13px;">请耐心等待，AI 正在逐条审阅合同条款</p>
      <p style="color:#999;font-size:12px;margin-top:4px;">已用时 {{ elapsed }} 秒</p>
      <div style="margin-top:20px;max-width:320px;margin-left:auto;margin-right:auto;">
        <div style="height:6px;background:#e0e7ff;border-radius:3px;overflow:hidden;">
          <div style="height:100%;background:linear-gradient(90deg,#4f46e5,#818cf8);border-radius:3px;transition:width 0.5s ease;" :style="{ width: progress + '%' }"></div>
        </div>
      </div>
    </div>

    <!-- Completed -->
    <div v-else-if="stage === 'completed'" style="background:#fff;border-radius:12px;padding:48px;border:1px solid #dcfce7;">
      <svg viewBox="0 0 80 80" style="width:80px;height:80px;">
        <circle cx="40" cy="40" r="32" fill="#dcfce7" stroke="#22c55e" stroke-width="2"/>
        <path d="M28 40 l8 8 l16 -16" fill="none" stroke="#22c55e" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      <h2 style="font-size:18px;margin:20px 0 8px;">审查完成</h2>
      <div style="margin-top:24px;display:flex;gap:12px;justify-content:center;">
        <n-button type="primary" size="large" @click="viewReport">查看审查报告</n-button>
        <n-button @click="goBack">返回上传</n-button>
      </div>
    </div>

    <!-- Failed -->
    <div v-else-if="stage === 'failed'" style="background:#fff;border-radius:12px;padding:48px;border:1px solid #fee2e2;">
      <n-icon size="56" color="#dc2626">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>
      </n-icon>
      <h2 style="font-size:18px;margin:16px 0 8px;">审查失败</h2>
      <p style="color:#666;font-size:14px;">{{ errorMessage }}</p>
      <div style="margin-top:24px;display:flex;gap:12px;justify-content:center;">
        <n-button type="primary" @click="retry">重新审查</n-button>
        <n-button @click="goBack">返回上传</n-button>
      </div>
    </div>

    <!-- No pending file -->
    <div v-else style="background:#fff;border-radius:12px;padding:48px;border:1px solid #eee;">
      <h2 style="font-size:18px;">没有待审查的合同</h2>
      <p style="color:#666;font-size:14px;margin-top:8px;">请先上传合同文件</p>
      <n-button type="primary" style="margin-top:24px;" @click="goBack">去上传</n-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useMessage } from 'naive-ui'
import api from '../api/request'
import { pendingUpload } from '../stores/upload'

const router = useRouter()
const msg = useMessage()

type Stage = 'pending' | 'working' | 'completed' | 'failed'
const stage = ref<Stage>('pending')
const progress = ref(0)
const elapsed = ref(0)
const errorMessage = ref('')

let contractId = 0
let pollTimer: ReturnType<typeof setInterval> | undefined
let progressTimer: ReturnType<typeof setInterval> | undefined
let elapsedTimer: ReturnType<typeof setInterval> | undefined

async function uploadAndReview() {
  if (!pendingUpload.file) return

  stage.value = 'working'
  startProgress()

  const form = new FormData()
  form.append('file', pendingUpload.file)
  form.append('title', pendingUpload.title)

  try {
    const res = await api.post('/contracts/upload', form)
    contractId = res.data.id
    pendingUpload.file = null
    startPolling()
  } catch {
    stopTimers()
    stage.value = 'failed'
    errorMessage.value = '文件上传失败，请重试'
  }
}

function startProgress() {
  progress.value = 0
  elapsed.value = 0
  progressTimer = setInterval(() => {
    const remaining = 90 - progress.value
    progress.value += Math.max(remaining * 0.03, 0.5)
    if (progress.value >= 90) progress.value = 90
  }, 400)
  elapsedTimer = setInterval(() => { elapsed.value++ }, 1000)
}

function startPolling() {
  pollTimer = setInterval(pollStatus, 1500)
  pollStatus()
}

async function pollStatus() {
  if (!contractId) return
  try {
    const res = await api.get(`/contracts/${contractId}`)
    const s: string = res.data.status

    if (s === 'completed') {
      stopTimers()
      progress.value = 100
      setTimeout(() => { stage.value = 'completed' }, 500)
    } else if (s === 'failed') {
      stopTimers()
      stage.value = 'failed'
      errorMessage.value = res.data.conclusion || 'AI 审查过程出现异常，请重试'
    }
  } catch {
    // ignore
  }
}

function stopTimers() {
  if (pollTimer) clearInterval(pollTimer)
  if (progressTimer) clearInterval(progressTimer)
  if (elapsedTimer) clearInterval(elapsedTimer)
  pollTimer = undefined
  progressTimer = undefined
  elapsedTimer = undefined
}

function retry() {
  stage.value = 'pending'
  progress.value = 0
  errorMessage.value = ''
  uploadAndReview()
}

function viewReport() {
  if (contractId) router.replace(`/contracts/${contractId}`)
}

function goBack() {
  pendingUpload.file = null
  router.replace('/')
}

onMounted(() => {
  if (pendingUpload.file) {
    uploadAndReview()
  } else {
    stage.value = 'pending'
  }
})

onUnmounted(() => {
  stopTimers()
})
</script>
