<template>
  <div class="risk-card" :class="'level-' + risk.risk_level">
    <div class="card-header">
      <div class="header-left">
        <span class="risk-badge" :class="'badge-' + risk.risk_level">
          {{ levelLabel }}
        </span>
        <span class="risk-category">{{ risk.category }}</span>
      </div>
      <div class="header-right">
        <span class="clause-ref">第{{ risk.clause_index }}条</span>
      </div>
    </div>

    <div class="card-body">
      <div class="field clause-text">
        <span class="field-label">原文</span>
        <span class="field-value">{{ risk.clause_text }}</span>
      </div>

      <div class="field description" :class="'desc-' + risk.risk_level">
        <span class="field-label">风险分析</span>
        <span class="field-value">{{ risk.description }}</span>
      </div>

      <div class="field suggestion">
        <span class="field-label">修改建议</span>
        <span class="field-value">{{ risk.suggestion }}</span>
      </div>

      <div v-if="risk.legal_basis" class="field legal-basis">
        <span class="field-label">法律依据</span>
        <span class="field-value">{{ risk.legal_basis }}</span>
      </div>
    </div>

    <div class="card-footer">
      <n-button
        v-if="risk.status === 'active'"
        size="tiny"
        quaternary
        @click="updateStatus('ignored')"
      >忽略</n-button>
      <n-button
        v-if="risk.status === 'active'"
        size="tiny"
        type="primary"
        @click="updateStatus('fixed')"
      >标记已处理</n-button>
      <span v-if="risk.status === 'ignored'" class="status-tag ignored">已忽略</span>
      <span v-if="risk.status === 'fixed'" class="status-tag fixed">已处理</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { riskApi } from '../api/risks'

const props = defineProps<{
  risk: any
}>()

const emit = defineEmits<{ (e: 'updated'): void }>()

const levelLabel = computed(() =>
  props.risk.risk_level === 'high' ? '高风险'
    : props.risk.risk_level === 'medium' ? '警告'
    : '提示'
)

async function updateStatus(status: string) {
  await riskApi.updateStatus(props.risk.contract_id, props.risk.id, status)
  emit('updated')
}
</script>

<style scoped>
.risk-card {
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #e5e7eb;
  transition: box-shadow 0.15s;
}

.risk-card:hover {
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.risk-card.level-high { border-left: 3px solid #ef4444; }
.risk-card.level-medium { border-left: 3px solid #f59e0b; }
.risk-card.level-low { border-left: 3px solid #3b82f6; }

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 14px;
  background: #f9fafb;
  border-bottom: 1px solid #f0f0f0;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.risk-badge {
  font-size: 11px;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 4px;
  color: #fff;
}

.badge-high { background: #ef4444; }
.badge-medium { background: #f59e0b; color: #fff; }
.badge-low { background: #3b82f6; }

.risk-category {
  font-size: 12px;
  color: #666;
}

.clause-ref {
  font-size: 11px;
  color: #999;
}

.card-body {
  padding: 12px 14px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  background: #fff;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.field-label {
  font-size: 11px;
  font-weight: 600;
  color: #999;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.field-value {
  font-size: 13px;
  line-height: 1.6;
  color: #333;
}

.description .field-value {
  padding: 8px 10px;
  border-radius: 6px;
  font-size: 13px;
}

.desc-high .field-value {
  background: #fef2f2;
  color: #991b1b;
}

.desc-medium .field-value {
  background: #fffbeb;
  color: #92400e;
}

.suggestion .field-value {
  background: #f0fdf4;
  color: #166534;
  padding: 8px 10px;
  border-radius: 6px;
}

.legal-basis .field-value {
  font-size: 12px;
  color: #1e40af;
  line-height: 1.5;
}

.card-footer {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
  padding: 8px 14px;
  background: #fafafa;
  border-top: 1px solid #f0f0f0;
}

.status-tag {
  font-size: 12px;
  padding: 2px 10px;
  border-radius: 4px;
  font-weight: 500;
}

.status-tag.ignored {
  background: #f3f4f6;
  color: #9ca3af;
}

.status-tag.fixed {
  background: #d1fae5;
  color: #065f46;
}
</style>
