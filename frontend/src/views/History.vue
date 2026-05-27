<template>
  <div>
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:24px;">
      <h2 style="font-size:20px;">审查历史记录</h2>
      <n-input v-model:value="search" placeholder="搜索合同名称" style="width:300px;" clearable @input="debounceSearch">
        <template #prefix>
          <n-icon><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg></n-icon>
        </template>
      </n-input>
    </div>
    <n-table :bordered="false" :single-line="false">
      <thead>
        <tr>
          <th>合同名称</th>
          <th>上传时间</th>
          <th>风险等级</th>
          <th>合规评分</th>
          <th style="text-align:right;">操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="c in contracts" :key="c.id">
          <td><strong>{{ c.title }}</strong></td>
          <td style="color:#999;font-size:13px;">{{ formatDate(c.created_at) }}</td>
          <td>
            <n-tag v-if="c.risk_level" size="small" :color="riskColor(c.risk_level)">{{ riskLabel(c.risk_level) }}</n-tag>
          </td>
          <td>
            <span :style="{ fontWeight: 600, color: scoreColor(c.compliance_score) }">{{ c.compliance_score ?? '-' }}</span>
          </td>
          <td style="text-align:right;">
            <router-link :to="`/contracts/${c.id}`"><n-button size="small" quaternary>工作台</n-button></router-link>
            <router-link :to="`/contracts/${c.id}/report`"><n-button size="small" quaternary>报告</n-button></router-link>
          </td>
        </tr>
      </tbody>
    </n-table>
    <div v-if="!contracts.length && !loading" style="text-align:center;padding:40px;color:#999;">暂无审查记录</div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { contractApi } from '../api/contracts'

const contracts = ref<any[]>([])
const search = ref('')
const loading = ref(false)
let debounceTimer: ReturnType<typeof setTimeout> | null = null

function riskColor(level: string) {
  return level === 'high' ? '#dc2626' : level === 'medium' ? '#d97706' : '#16a34a'
}
function riskLabel(level: string) {
  return level === 'high' ? '高风险' : level === 'medium' ? '中风险' : '低风险'
}
function scoreColor(score: number | null) {
  if (score == null) return '#999'
  return score >= 80 ? '#16a34a' : score >= 60 ? '#d97706' : '#dc2626'
}
function formatDate(dateStr: string) {
  return dateStr ? dateStr.slice(0, 10) : ''
}

function debounceSearch() {
  if (debounceTimer) clearTimeout(debounceTimer)
  debounceTimer = setTimeout(fetchList, 300)
}

async function fetchList() {
  loading.value = true
  try {
    const res = await contractApi.list({ search: search.value, page: 1, page_size: 50 })
    contracts.value = res.data.items || []
  } catch { /* ignore */ } finally {
    loading.value = false
  }
}

onMounted(fetchList)
</script>
