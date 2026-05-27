<template>
  <div style="display:grid;grid-template-columns:2fr 1fr;gap:24px;">
    <div style="background:#fff;border-radius:12px;padding:32px;border:1px solid #eee;">
      <h2 style="font-size:18px;margin-bottom:24px;">上传新合同</h2>
      <FileUploader @file-selected="onFileSelected" />
      <n-input v-model:value="contractTitle" placeholder="合同名称（可选）" style="margin-top:16px;" />
      <n-button type="primary" size="large" block style="margin-top:16px;" :loading="uploading" :disabled="!selectedFile" @click="startReview">
        开始智能审查
      </n-button>
    </div>
    <div style="background:#f0f7ff;border-radius:12px;padding:24px;border:1px solid #dbeafe;">
      <h3 style="font-size:15px;margin-bottom:12px;">审查说明</h3>
      <ul style="font-size:13px;color:#555;line-height:1.8;padding-left:16px;">
        <li>支持 PDF、Word 文档格式</li>
        <li>系统将自动匹配法规及行业标准</li>
        <li>重点审查履约期限、违约责任及争议解决条款</li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useMessage } from 'naive-ui'
import api from '../api/request'
import FileUploader from '../components/FileUploader.vue'

const router = useRouter()
const msg = useMessage()
const selectedFile = ref<File | null>(null)
const contractTitle = ref('')
const uploading = ref(false)

function onFileSelected(file: File | null) { selectedFile.value = file }

async function startReview() {
  if (!selectedFile.value) return
  uploading.value = true
  try {
    const form = new FormData()
    form.append('file', selectedFile.value)
    form.append('title', contractTitle.value)
    const res = await api.post('/contracts/upload', form)
    msg.success('审查完成')
    router.push(`/contracts/${res.data.id}`)
  } catch {
    msg.error('审查失败，请重试')
  } finally {
    uploading.value = false
  }
}
</script>
