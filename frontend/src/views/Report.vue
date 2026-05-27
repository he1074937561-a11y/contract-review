<template>
  <div style="max-width:900px;margin:0 auto;background:#fff;border-radius:12px;padding:48px;box-shadow:0 1px 8px rgba(0,0,0,0.06);">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:32px;border-bottom:2px solid #1e3a8a;padding-bottom:16px;">
      <div>
        <h2 style="font-size:22px;color:#1e3a8a;">智审通 AI</h2>
        <p style="font-size:10px;color:#999;">Intelligent Contract Review System</p>
      </div>
      <div style="text-align:right;">
        <p style="font-size:12px;color:#999;">{{ report?.report_number }}</p>
        <n-button type="primary" size="small" style="margin-top:8px;" @click="exportPdf">导出 PDF</n-button>
      </div>
    </div>
    <div v-if="loading" style="text-align:center;padding:60px;">
      <n-spin size="large" />
    </div>
    <div v-else>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:32px;">
        <div style="background:#f9fafb;padding:16px;border-radius:8px;">
          <span style="color:#999;font-size:12px;">合同名称</span>
          <p style="font-weight:600;margin-top:4px;">{{ contract.title }}</p>
        </div>
        <div style="background:#f9fafb;padding:16px;border-radius:8px;">
          <span style="color:#999;font-size:12px;">合规评分</span>
          <p :style="{ fontWeight: 600, fontSize: '24px', color: scoreColor }">{{ contract.compliance_score ?? '-' }} / 100</p>
        </div>
      </div>

      <h3 style="font-size:16px;margin-bottom:16px;border-left:4px solid #1e3a8a;padding-left:12px;">核心风险清单</h3>
      <div v-for="r in risks" :key="r.id" style="padding:12px 16px;background:#f9f9f9;border-radius:8px;margin-bottom:8px;">
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;">
          <n-tag size="small" :color="tagColor(r.risk_level)">{{ tagLabel(r.risk_level) }}</n-tag>
          <span style="font-weight:600;font-size:14px;">{{ r.category }}</span>
        </div>
        <p style="font-size:13px;color:#666;line-height:1.6;">{{ r.description }}</p>
        <p v-if="r.suggestion" style="font-size:12px;color:#92400e;margin-top:4px;">💡 {{ r.suggestion }}</p>
      </div>
      <div v-if="!risks.length" style="text-align:center;padding:24px;color:#999;">暂无风险项</div>

      <div v-if="contract.conclusion" style="margin-top:24px;padding-top:16px;border-top:1px solid #eee;">
        <h4 style="font-size:14px;color:#999;margin-bottom:8px;">审查结论</h4>
        <p style="font-size:13px;line-height:1.8;color:#444;">{{ contract.conclusion }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { contractApi } from '../api/contracts'
import { riskApi } from '../api/risks'
import api from '../api/request'

const route = useRoute()
const contract = ref<any>({})
const risks = ref<any[]>([])
const report = ref<any>(null)
const loading = ref(true)

const scoreColor = computed(() => {
  const s = contract.value.compliance_score || 0
  return s >= 80 ? '#16a34a' : s >= 60 ? '#d97706' : '#dc2626'
})

function tagColor(level: string) {
  return level === 'high' ? '#dc2626' : level === 'medium' ? '#d97706' : '#2563eb'
}
function tagLabel(level: string) {
  return level === 'high' ? '高风险' : level === 'medium' ? '警告' : '提示'
}

async function exportPdf() {
  window.open(`http://localhost:8000/api/contracts/${route.params.id}/report/export`, '_blank')
}

onMounted(async () => {
  try {
    const [c, r, rep] = await Promise.all([
      contractApi.get(Number(route.params.id)),
      riskApi.list(Number(route.params.id)),
      api.get(`/contracts/${route.params.id}/report`),
    ])
    contract.value = c.data
    risks.value = r.data
    report.value = rep.data
  } catch { /* ignore */ } finally {
    loading.value = false
  }
})
</script>
