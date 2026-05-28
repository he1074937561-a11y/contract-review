<template>
  <div style="max-width:900px;margin:0 auto;background:#fff;border-radius:12px;padding:48px;box-shadow:0 1px 8px rgba(0,0,0,0.06);">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:32px;border-bottom:2px solid #1e3a8a;padding-bottom:16px;">
      <div>
        <h2 style="font-size:22px;color:#1e3a8a;">智审通 AI</h2>
        <p style="font-size:10px;color:#999;">Intelligent Contract Review System</p>
      </div>
      <div style="text-align:right;">
        <p style="font-size:12px;color:#999;">{{ report?.report_number }}</p>
        <div style="display:flex;gap:8px;margin-top:8px;">
          <n-button size="small" @click="exportPdf">导出报告</n-button>
        </div>
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
      <div v-for="r in risks" :key="r.id" class="risk-item-report">
        <div style="display:flex;align-items:flex-start;justify-content:space-between;">
          <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">
            <n-tag size="small" :color="tagColor(r.risk_level)">{{ tagLabel(r.risk_level) }}</n-tag>
            <span style="font-weight:600;font-size:14px;">{{ r.category }}</span>
            <n-tag v-if="r.clause_index" size="small" bordered>第{{ r.clause_index }}条</n-tag>
          </div>
          <n-tag size="small" :type="statusType(r.status)" bordered>{{ statusLabel(r.status) }}</n-tag>
        </div>
        <p style="font-size:13px;color:#666;line-height:1.6;margin-top:6px;">{{ r.description }}</p>
        <p v-if="r.suggestion" style="font-size:12px;color:#92400e;margin-top:4px;">💡 {{ r.suggestion }}</p>
        <div style="margin-top:6px;">
          <n-select
            :value="r.status"
            :options="statusOptions"
            size="tiny"
            style="width:130px;"
            :render-label="renderStatusLabel"
            @update:value="(v: string) => updateRisk(r, v)"
          />
        </div>
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
import { ref, computed, onMounted, h } from 'vue'
import { useRoute } from 'vue-router'
import { useMessage } from 'naive-ui'
import { contractApi } from '../api/contracts'
import { riskApi } from '../api/risks'
import api from '../api/request'

const route = useRoute()
const msg = useMessage()
const contract = ref<any>({})
const risks = ref<any[]>([])
const report = ref<any>(null)
const loading = ref(true)

const scoreColor = computed(() => {
  const s = contract.value.compliance_score || 0
  return s >= 80 ? '#16a34a' : s >= 60 ? '#d97706' : '#dc2626'
})

const statusOptions = [
  { label: '待处理', value: 'active' },
  { label: '已处理', value: 'fixed' },
  { label: '已忽略', value: 'ignored' },
]

const statusColors: Record<string, string> = {
  active: '#d97706',
  fixed: '#16a34a',
  ignored: '#9ca3af',
}

function statusType(s: string) {
  if (s === 'fixed') return 'success'
  if (s === 'ignored') return 'default'
  return 'warning'
}

function statusLabel(s: string) {
  if (s === 'fixed') return '已处理'
  if (s === 'ignored') return '已忽略'
  return '待处理'
}

function renderStatusLabel(option: any) {
  const color = statusColors[option.value as string] || '#999'
  return h('span', { style: 'display:inline-flex;align-items:center;gap:6px;' }, [
    h('span', { style: `display:inline-block;width:8px;height:8px;border-radius:50%;background:${color};` }),
    option.label as string,
  ])
}

function tagColor(level: string) {
  return level === 'high' ? '#dc2626' : level === 'medium' ? '#d97706' : '#2563eb'
}
function tagLabel(level: string) {
  return level === 'high' ? '高风险' : level === 'medium' ? '警告' : '提示'
}

async function exportPdf() {
  try {
    const res = await api.post(`/contracts/${route.params.id}/report/export`, {}, { responseType: 'blob' })
    const url = URL.createObjectURL(res.data)
    window.open(url, '_blank')
    setTimeout(() => URL.revokeObjectURL(url), 60000)
  } catch {
    msg.error('导出报告失败')
  }
}

async function updateRisk(r: any, status: string) {
  try {
    await riskApi.updateStatus(r.contract_id, r.id, status)
    r.status = status
  } catch {
    msg.error('操作失败')
  }
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

<style scoped>
.risk-item-report {
  padding: 14px 16px;
  background: #f9f9f9;
  border-radius: 8px;
  margin-bottom: 8px;
  border: 1px solid #eee;
  transition: box-shadow 0.15s;
}
.risk-item-report:hover {
  box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
</style>
