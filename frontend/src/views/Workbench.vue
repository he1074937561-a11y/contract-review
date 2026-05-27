<template>
  <div v-if="loading" style="text-align:center;padding:80px;">
    <n-spin size="large" />
    <p style="color:#999;margin-top:16px;">正在加载审查结果...</p>
  </div>
  <div v-else style="display:flex;gap:0;height:calc(100vh - 120px);border-radius:8px;overflow:hidden;">
    <!-- Left panel: Contract text viewer -->
    <div style="flex:1;overflow-y:auto;padding:16px;background:#f0f2f5;border-right:1px solid #e0e0e0;">
      <ContractViewer :title="contract.title" :segments="segments" @risk-click="scrollToRisk" />
    </div>
    <!-- Right panel: Risks + Chat -->
    <div style="width:440px;display:flex;flex-direction:column;background:#fff;">
      <div style="padding:12px 16px;border-bottom:1px solid #eee;display:flex;justify-content:space-between;align-items:center;">
        <span style="font-weight:bold;">风险列表 ({{ risks.length }})</span>
        <div style="display:flex;gap:8px;">
          <n-tag v-if="highCount" size="small" color="#ef4444">{{ highCount }} 高风险</n-tag>
          <n-tag v-if="mediumCount" size="small" color="#f59e0b">{{ mediumCount }} 警告</n-tag>
        </div>
      </div>
      <div style="flex:1;overflow-y:auto;padding:12px;display:flex;flex-direction:column;gap:12px;">
        <RiskCard v-for="r in risks" :key="r.id" :risk="r" @updated="fetchRisks" />
        <div v-if="!risks.length" style="text-align:center;color:#999;padding:40px;font-size:13px;">
          <p>暂无风险项</p>
        </div>
      </div>
      <!-- Chat input bar -->
      <div style="padding:12px;border-top:1px solid #eee;display:flex;gap:8px;">
        <n-input v-model:value="chatInput" placeholder="向 AI 询问关于此合同的问题..." :disabled="sendingChat" />
        <n-button type="primary" @click="sendChat" :loading="sendingChat">发送</n-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useMessage } from 'naive-ui'
import { contractApi } from '../api/contracts'
import { riskApi } from '../api/risks'
import api from '../api/request'
import ContractViewer from '../components/ContractViewer.vue'
import RiskCard from '../components/RiskCard.vue'

const route = useRoute()
const msg = useMessage()
const contract = ref<any>({})
const risks = ref<any[]>([])
const loading = ref(true)
const chatInput = ref('')
const sendingChat = ref(false)

const segments = computed(() => {
  if (!contract.value.raw_text) return []
  const text = contract.value.raw_text
  const riskMap = new Map<number, any>()
  risks.value.forEach(r => { riskMap.set(r.clause_index, r) })
  return text.split(/(\n)/).map((p: string) => {
    const risk = riskMap.get(0) // simplified highlighting
    return { text: p, risk: risk?.risk_level, riskId: risk?.id }
  })
})

const highCount = computed(() => risks.value.filter(r => r.risk_level === 'high').length)
const mediumCount = computed(() => risks.value.filter(r => r.risk_level === 'medium').length)

async function fetchRisks() {
  try {
    const res = await riskApi.list(Number(route.params.id))
    risks.value = res.data
  } catch { /* ignore */ }
}

async function sendChat() {
  if (!chatInput.value) return
  sendingChat.value = true
  try {
    const res = await api.post(`/contracts/${route.params.id}/chat`, { message: chatInput.value })
    msg.info('AI: ' + res.data.content.slice(0, 100) + '...')
  } catch {
    msg.error('发送失败')
  } finally {
    chatInput.value = ''
    sendingChat.value = false
  }
}

function scrollToRisk(id: number) {
  // Scroll could be implemented with scrollIntoView
}

onMounted(async () => {
  try {
    const res = await contractApi.get(Number(route.params.id))
    contract.value = res.data
    await fetchRisks()
  } catch {
    msg.error('加载合同失败')
  } finally {
    loading.value = false
  }
})
</script>
