<template>
  <div>
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:24px;">
      <h2 style="font-size:20px;">合同模板库</h2>
    </div>
    <div v-if="loading" style="text-align:center;padding:40px;"><n-spin size="large" /></div>
    <div v-else-if="!templates.length" style="text-align:center;padding:60px;background:#fff;border-radius:12px;border:1px solid #eee;color:#999;">
      <p>暂无模板</p>
    </div>
    <div v-else style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px;">
      <div v-for="t in templates" :key="t.id" style="background:#fff;border-radius:12px;padding:20px;border:1px solid #eee;transition:box-shadow 0.2s;">
        <p style="font-weight:600;">{{ t.name }}</p>
        <p v-if="t.type" style="font-size:12px;color:#1e3a8a;margin-top:4px;">{{ t.type }}</p>
        <p v-if="t.description" style="font-size:12px;color:#666;margin-top:8px;">{{ t.description }}</p>
        <p style="font-size:11px;color:#999;margin-top:8px;">下载 {{ t.download_count }} 次</p>
        <n-button size="small" style="margin-top:12px;">下载模板</n-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '../api/request'

const templates = ref<any[]>([])
const loading = ref(true)

onMounted(async () => {
  try {
    const res = await api.get('/templates')
    templates.value = res.data
  } catch { /* ignore */ } finally {
    loading.value = false
  }
})
</script>
