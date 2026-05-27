<template>
  <div :style="{
    border: `2px solid ${borderColor}`,
    borderRadius: '12px',
    overflow: 'hidden',
    boxShadow: '0 1px 4px rgba(0,0,0,0.06)',
  }">
    <div :style="{ background: headerBg, padding: '8px 12px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }">
      <span style="color:#fff;font-size:12px;font-weight:bold;">
        {{ levelLabel }} · {{ risk.category }}
      </span>
      <span style="color:rgba(255,255,255,0.8);font-size:11px;">第{{ risk.clause_index }}条</span>
    </div>
    <div style="padding:12px;background:#fff;">
      <div style="font-size:13px;color:#666;margin-bottom:8px;">
        <span style="font-weight:bold;color:#333;">原文：</span>{{ risk.clause_text }}
      </div>
      <div v-if="risk.description" :style="{ padding: '8px', borderRadius: '8px', fontSize: '13px', marginBottom: '8px', background: descBg, color: descColor }">
        {{ risk.description }}
      </div>
      <div v-if="risk.legal_basis" style="font-size:12px;color:#1e40af;margin-bottom:8px;">
        ⚖ {{ risk.legal_basis }}
      </div>
      <div v-if="risk.suggestion" style="font-size:12px;color:#92400e;padding:6px 8px;background:#fffbeb;border-radius:6px;margin-bottom:8px;">
        💡 {{ risk.suggestion }}
      </div>
      <div style="display:flex;gap:8px;justify-content:flex-end;border-top:1px solid #f0f0f0;padding-top:8px;">
        <n-button size="tiny" quaternary @click="updateStatus('ignored')">忽略</n-button>
        <n-button v-if="risk.status==='active'" size="tiny" type="primary" @click="updateStatus('fixed')">标记已处理</n-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { riskApi } from '../api/risks'

const props = defineProps<{
  risk: {
    id: number
    contract_id: number
    clause_index: number
    clause_text: string
    risk_level: string
    category: string
    description: string
    legal_basis: string
    suggestion: string
    status: string
  }
}>()

const emit = defineEmits<{ (e: 'updated'): void }>()

const borderColor = computed(() =>
  props.risk.risk_level === 'high' ? '#ef4444' : props.risk.risk_level === 'medium' ? '#f59e0b' : '#3b82f6'
)
const headerBg = computed(() =>
  props.risk.risk_level === 'high' ? '#dc2626' : props.risk.risk_level === 'medium' ? '#d97706' : '#2563eb'
)
const levelLabel = computed(() =>
  props.risk.risk_level === 'high' ? '高风险' : props.risk.risk_level === 'medium' ? '警告' : '提示'
)
const descBg = computed(() =>
  props.risk.risk_level === 'high' ? '#fef2f2' : '#fffbeb'
)
const descColor = computed(() =>
  props.risk.risk_level === 'high' ? '#991b1b' : '#92400e'
)

async function updateStatus(status: string) {
  await riskApi.updateStatus(props.risk.contract_id, props.risk.id, status)
  emit('updated')
}
</script>
