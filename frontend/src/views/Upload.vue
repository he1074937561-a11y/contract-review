<template>
  <div>
    <div style="display:grid;grid-template-columns:2fr 1fr;gap:24px;">
      <div style="background:#fff;border-radius:12px;padding:32px;border:1px solid #eee;">
        <h2 style="font-size:18px;margin-bottom:24px;">上传新合同</h2>
        <FileUploader @file-selected="onFileSelected" />
        <n-input v-model:value="contractTitle" placeholder="合同名称（可选）" style="margin-top:16px;" />
        <n-button type="primary" size="large" block style="margin-top:16px;" :disabled="!selectedFile || uploading" @click="startReview">
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

    <!-- Recent uploads -->
    <div style="background:#fff;border-radius:12px;padding:24px;border:1px solid #eee;margin-top:24px;">
      <h3 style="font-size:15px;margin-bottom:16px;">最近上传</h3>
      <div v-if="loading" style="text-align:center;padding:20px;color:#999;">
        <n-spin size="small" /> <span style="margin-left:8px;">加载中...</span>
      </div>
      <div v-else-if="recentList.length === 0" style="text-align:center;padding:20px;color:#ccc;font-size:14px;">
        暂无上传记录
      </div>
      <div v-else>
        <div v-for="item in recentList" :key="item.id"
          style="display:flex;align-items:center;justify-content:space-between;padding:10px 0;border-bottom:1px solid #f5f5f5;cursor:pointer;"
          @click="goContract(item)">
          <div style="display:flex;align-items:center;gap:12px;">
            <span style="font-size:20px;">{{ fileIcon(item.file_type) }}</span>
            <div>
              <p style="font-weight:600;font-size:14px;">{{ item.title }}</p>
              <p style="color:#999;font-size:12px;">{{ formatTime(item.created_at) }}</p>
            </div>
          </div>
          <n-tag :type="statusType(item.status)" size="small">{{ statusLabel(item.status) }}</n-tag>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import FileUploader from '../components/FileUploader.vue'
import { pendingUpload } from '../stores/upload'
import api from '../api/request'

const router = useRouter()
const selectedFile = ref<File | null>(null)
const contractTitle = ref('')
const uploading = ref(false)
const recentList = ref<any[]>([])
const loading = ref(true)

function onFileSelected(file: File | null) { selectedFile.value = file }

function startReview() {
  if (!selectedFile.value) return
  pendingUpload.file = selectedFile.value
  pendingUpload.title = contractTitle.value
  router.push('/review')
}

function fileIcon(type: string) {
  return type === 'pdf' ? '📄' : '📝'
}

function formatTime(t: string) {
  return t?.slice(0, 10) || ''
}

function statusType(s: string) {
  if (s === 'completed') return 'success'
  if (s === 'failed') return 'error'
  return 'warning'
}

function statusLabel(s: string) {
  if (s === 'completed') return '审查完成'
  if (s === 'reviewing') return '审查中'
  if (s === 'failed') return '审查失败'
  return '待审查'
}

function goContract(item: any) {
  if (item.status === 'completed' || item.status === 'failed') {
    router.push(`/contracts/${item.id}`)
  } else {
    router.push(`/review`)
  }
}

onMounted(async () => {
  try {
    const res = await api.get('/contracts', { params: { page: 1, page_size: 5 } })
    recentList.value = res.data.items || []
  } catch {
    recentList.value = []
  } finally {
    loading.value = false
  }
})
</script>
