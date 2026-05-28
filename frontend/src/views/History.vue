<template>
  <div>
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-bottom:24px;">
      <div style="background:#fff;border-radius:12px;padding:20px 24px;border:1px solid #e5e7eb;display:flex;align-items:center;gap:16px;">
        <div style="width:44px;height:44px;background:#eef2ff;border-radius:12px;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
          <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="#4f46e5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/>
          </svg>
        </div>
        <div>
          <p style="font-size:12px;color:#94a3b8;margin:0;">审查总数</p>
          <p style="font-size:28px;font-weight:700;color:#1e293b;margin:2px 0 0;">{{ stats.total_contracts }}</p>
        </div>
      </div>
      <div style="background:#fff;border-radius:12px;padding:20px 24px;border:1px solid #fecaca;display:flex;align-items:center;gap:16px;">
        <div style="width:44px;height:44px;background:#fef2f2;border-radius:12px;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
          <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="#dc2626" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>
          </svg>
        </div>
        <div>
          <p style="font-size:12px;color:#94a3b8;margin:0;">高风险合同</p>
          <p style="font-size:28px;font-weight:700;color:#dc2626;margin:2px 0 0;">{{ stats.high_risk }}</p>
        </div>
      </div>
      <div style="background:#fff;border-radius:12px;padding:20px 24px;border:1px solid #dbeafe;display:flex;align-items:center;gap:16px;">
        <div style="width:44px;height:44px;background:#eff6ff;border-radius:12px;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
          <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="#2563eb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
          </svg>
        </div>
        <div>
          <p style="font-size:12px;color:#94a3b8;margin:0;">平均合规分</p>
          <p style="font-size:28px;font-weight:700;color:#2563eb;margin:2px 0 0;">{{ stats.avg_score }}</p>
        </div>
      </div>
    </div>
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
          <td>
            <n-tooltip trigger="hover">
              <template #trigger>
                <span style="font-weight:600;cursor:pointer;color:#1e3a8a;" @click="viewOriginal(c)">{{ c.title }}</span>
              </template>
              查看原件
            </n-tooltip>
          </td>
          <td style="color:#999;font-size:13px;">{{ formatDate(c.created_at) }}</td>
          <td>
            <n-tag v-if="c.risk_level" size="small" :color="riskColor(c.risk_level)">{{ riskLabel(c.risk_level) }}</n-tag>
          </td>
          <td>
            <span :style="{ fontWeight: 600, color: scoreColor(c.compliance_score) }">{{ c.compliance_score ?? '-' }}</span>
          </td>
          <td style="text-align:right;white-space:nowrap;">
            <router-link :to="`/contracts/${c.id}`"><n-button size="small" quaternary>工作台</n-button></router-link>
            <router-link :to="`/contracts/${c.id}/report`"><n-button size="small" quaternary>报告</n-button></router-link>
            <n-button size="small" quaternary type="error" @click="openDelete(c)">删除</n-button>
          </td>
        </tr>
      </tbody>
    </n-table>
    <div v-if="!contracts.length && !loading" style="text-align:center;padding:40px;color:#999;">暂无审查记录</div>
    <div v-if="total > pageSize" style="display:flex;justify-content:flex-end;margin-top:20px;">
      <n-pagination
        :page="page"
        :page-count="pageCount"
        :page-size="pageSize"
        @update:page="onPageChange"
      />
    </div>

    <!-- Delete confirmation modal -->
    <n-modal v-model:show="showDeleteModal" preset="dialog" :mask-closable="false" @update:show="onModalClose">
      <template #icon>
        <n-icon color="#d97706" size="24">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
        </n-icon>
      </template>
      <template #header>
        <span style="font-size:16px;">确定删除此合同？</span>
      </template>
      <p style="color:#999;font-size:13px;margin:0;">删除后不可恢复，相关审查数据将一并清除。</p>
      <template #action>
        <n-button size="small" @click="showDeleteModal = false">取消</n-button>
        <n-button size="small" type="error" :loading="deleting" @click="confirmDelete">删除</n-button>
      </template>
    </n-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useMessage } from 'naive-ui'
import { contractApi } from '../api/contracts'
import api from '../api/request'

const msg = useMessage()
const contracts = ref<any[]>([])
const stats = ref({ total_contracts: 0, high_risk: 0, avg_score: 0 })
const search = ref('')
const loading = ref(false)
const page = ref(1)
const total = ref(0)
const pageSize = 20
const deleteTarget = ref<any>(null)
const showDeleteModal = ref(false)
const deleting = ref(false)
let debounceTimer: ReturnType<typeof setTimeout> | null = null

const pageCount = computed(() => Math.ceil(total.value / pageSize))

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
  debounceTimer = setTimeout(() => {
    page.value = 1
    fetchList()
  }, 300)
}

function onPageChange(p: number) {
  page.value = p
  fetchList()
}

function openDelete(c: any) {
  deleteTarget.value = c
  showDeleteModal.value = true
}

function onModalClose(show: boolean) {
  if (!show) deleteTarget.value = null
}

async function confirmDelete() {
  if (!deleteTarget.value) return
  deleting.value = true
  try {
    await contractApi.delete(deleteTarget.value.id)
    msg.success('已删除')
    showDeleteModal.value = false
    deleteTarget.value = null
    fetchList()
  } catch {
    msg.error('删除失败')
  } finally {
    deleting.value = false
  }
}

async function viewOriginal(c: any) {
  try {
    const res = await api.get(`/contracts/${c.id}/file`, { responseType: 'blob' })
    const url = URL.createObjectURL(res.data)
    window.open(url, '_blank')
    setTimeout(() => URL.revokeObjectURL(url), 60000)
  } catch {
    msg.error('查看原件失败')
  }
}

async function fetchList() {
  loading.value = true
  try {
    const res = await contractApi.list({ search: search.value, page: page.value, page_size: pageSize })
    contracts.value = res.data.items || []
    total.value = res.data.total || 0
  } catch { /* ignore */ } finally {
    loading.value = false
  }
}

onMounted(async () => {
  fetchList()
  try {
    const s = await api.get('/admin/stats')
    stats.value = s.data
  } catch { /* ignore */ }
})
</script>
