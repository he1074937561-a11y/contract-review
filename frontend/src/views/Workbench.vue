<template>
  <div v-if="loading" class="loading-state">
    <n-spin size="large" />
    <p>正在加载审查结果...</p>
  </div>
  <div v-else class="workbench">
    <!-- Left: Contract document with risk highlights -->
    <div class="left-panel">
      <div class="contract-doc">
        <h2 class="doc-title">{{ contract.title }}</h2>
        <div class="doc-body">
          <div v-for="(seg, i) in segments" :key="i"
            :class="['doc-line', { 'has-risk': seg.risk, 'section-title': seg.isSection, 'is-empty': !seg.text.trim() }]"
            @click="seg.risk && scrollToRisk(seg.riskId)"
          >
            <span v-if="seg.risk" class="risk-tag" :class="'tag-' + seg.risk">{{ seg.riskIdx }}</span>
            <span class="line-text">{{ seg.text }}</span>
          </div>
        </div>
        <div v-if="!segments.length" class="empty-state">暂无合同原文</div>
      </div>
    </div>
    <!-- Right: Risk list grouped by category -->
    <div class="right-panel">
      <div class="panel-header">
        <span class="panel-title">审查结果</span>
        <div class="count-group">
          <span class="count high">{{ highCount }} 高风险</span>
          <span class="count medium">{{ mediumCount }} 警告</span>
        </div>
      </div>
      <div ref="riskBodyRef" class="panel-body">
        <div v-if="!risks.length" class="empty-hint">暂无风险项</div>
        <div v-for="(group, cat) in groupedRisks" :key="cat" class="risk-group">
          <div class="group-label">{{ cat }}（{{ group.length }}）</div>
          <div v-for="r in group" :key="r.id" :data-risk-id="r.id" :class="['risk-item', 'level-' + r.risk_level, { 'risk-highlighted': highlightedId === r.id }]">
            <div class="item-header">
              <span class="risk-tag" :class="'tag-' + r.risk_level">{{ r._idx }}</span>
              <span class="item-pos">第{{ r.clause_index }}条</span>
              <span v-if="r.status === 'fixed'" class="item-status fixed">已处理</span>
              <span v-if="r.status === 'ignored'" class="item-status ignored">已忽略</span>
            </div>
            <div class="item-desc">{{ r.description }}</div>
            <div v-if="r.suggestion" class="item-suggestion">💡 {{ r.suggestion }}</div>
            <div v-if="r.legal_basis" class="item-law">{{ r.legal_basis }}</div>
            <div v-if="r.status === 'active'" class="item-actions">
              <n-button size="tiny" quaternary @click="updateRisk(r, 'ignored')">忽略</n-button>
              <n-button size="tiny" type="primary" @click="updateRisk(r, 'fixed')">标记已处理</n-button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- Robot icon -->
    <div class="robot-btn" @click="chatOpen = true">
      <svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <rect x="3" y="11" width="18" height="10" rx="2"/>
        <circle cx="12" cy="16" r="1" fill="currentColor"/>
        <path d="M8 11V7a4 4 0 0 1 8 0v4"/>
        <line x1="9" y1="5" x2="7" y2="3"/>
        <line x1="15" y1="5" x2="17" y2="3"/>
      </svg>
    </div>
    <!-- AI Chat side panel -->
    <Transition name="slide">
      <div v-if="chatOpen" class="chat-overlay" @click.self="chatOpen = false">
        <div class="chat-panel">
          <div class="chat-header">
            <div class="chat-header-left">
              <span class="chat-header-icon">
                <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="3" y="11" width="18" height="10" rx="2"/><circle cx="12" cy="16" r="1" fill="currentColor"/>
                  <path d="M8 11V7a4 4 0 0 1 8 0v4"/>
                </svg>
              </span>
              <div>
                <div class="chat-title">智审通小助手</div>
                <div class="chat-subtitle">基于合同上下文的智能问答</div>
              </div>
            </div>
            <n-button quaternary circle size="tiny" @click="chatOpen = false" class="chat-close-btn">
              <template #icon>
                <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
              </template>
            </n-button>
          </div>
          <div class="chat-messages" ref="msgListRef">
            <div v-if="!chatMessages.length" class="chat-welcome">
              <div class="welcome-icon">
                <svg viewBox="0 0 24 24" width="36" height="36" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="3" y="11" width="18" height="10" rx="2"/><circle cx="12" cy="16" r="1" fill="currentColor"/>
                  <path d="M8 11V7a4 4 0 0 1 8 0v4"/>
                </svg>
              </div>
              <p class="welcome-text">您好！我是智审通小助手</p>
              <p class="welcome-hint">您可以向我询问关于此合同的任何问题，例如：</p>
              <div class="welcome-suggestions">
                <span class="suggestion-tag" @click="quickQuestion('这份合同的主要风险是什么？')">这份合同的主要风险是什么？</span>
                <span class="suggestion-tag" @click="quickQuestion('第7条违约责任是否合理？')">第7条违约责任是否合理？</span>
                <span class="suggestion-tag" @click="quickQuestion('付款条款有没有对我方不利的地方？')">付款条款有没有对我方不利的地方？</span>
              </div>
            </div>
            <div v-for="(msg, i) in chatMessages" :key="i" :class="['msg', 'msg-' + msg.role]">
              <div class="msg-avatar">
                <svg v-if="msg.role === 'assistant'" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="3" y="11" width="18" height="10" rx="2"/><circle cx="12" cy="16" r="1" fill="currentColor"/>
                  <path d="M8 11V7a4 4 0 0 1 8 0v4"/>
                </svg>
                <svg v-else viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>
                </svg>
              </div>
              <div class="msg-body">
                <div class="msg-label">{{ msg.role === 'user' ? '你' : '智审通小助手' }}</div>
                <div class="msg-content" v-if="msg.role === 'assistant'" v-html="renderMarkdown(msg.content)"></div>
                <div class="msg-content" v-else>{{ msg.content }}</div>
              </div>
            </div>
            <div v-if="sendingChat" class="msg msg-assistant">
              <div class="msg-avatar">
                <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="3" y="11" width="18" height="10" rx="2"/><circle cx="12" cy="16" r="1" fill="currentColor"/>
                  <path d="M8 11V7a4 4 0 0 1 8 0v4"/>
                </svg>
              </div>
              <div class="msg-body">
                <div class="msg-label">智审通小助手</div>
                <div class="msg-content thinking">
                  <span class="dot-pulse"></span>
                  <span>正在思考...</span>
                </div>
              </div>
            </div>
          </div>
          <div class="chat-input-bar">
            <n-input v-model:value="chatInput" placeholder="输入您的问题..." :disabled="sendingChat" size="small" class="chat-input" @keyup.enter="sendChat" />
            <n-button type="primary" @click="sendChat" :loading="sendingChat" size="small" class="chat-send-btn">发送</n-button>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { useMessage } from 'naive-ui'
import { marked } from 'marked'
import { contractApi } from '../api/contracts'
import { riskApi } from '../api/risks'
import api from '../api/request'

const route = useRoute()
const msg = useMessage()
const contract = ref<any>({})
const risks = ref<any[]>([])
const loading = ref(true)
const chatInput = ref('')
const sendingChat = ref(false)
const highlightedId = ref<number | null>(null)
const riskBodyRef = ref<HTMLElement | null>(null)
const chatOpen = ref(false)
const chatMessages = ref<{ role: string; content: string }[]>([])
const msgListRef = ref<HTMLElement | null>(null)

const cnMap: Record<string, number> = {一:1,二:2,三:3,四:4,五:5,六:6,七:7,八:8,九:9,十:10}
const sectionRe = /^第([一二三四五六七八九十]+)条/

function renderMarkdown(text: string) {
  return marked.parse(text, { async: false }) as string
}

function parseClause(line: string): number | null {
  const t = line.trim()
  const m = t.match(/^(\d+(?:\.\d+)?)[\s.、]/)
  if (m) return parseFloat(m[1])
  const c = t.match(sectionRe)
  if (c) return c[1].split('').reduce((s, ch) => s + (cnMap[ch] || 0), 0)
  return null
}

const segments = computed(() => {
  if (!contract.value.raw_text) return []
  const lines = contract.value.raw_text.split('\n')
  const rMap = new Map<number, { level: string; id: number }>()
  risks.value.forEach((r) => {
    rMap.set(r.clause_index, { level: r.risk_level, id: r.id })
  })
  return lines.map((text: string) => {
    const idx = parseClause(text)
    const isSection = sectionRe.test(text.trim())
    const matched = idx !== null ? rMap.get(idx) : undefined
    let risk: string | undefined, riskId: number | undefined, riskIdx: string | undefined
    if (matched) {
      risk = matched.level
      riskId = matched.id
      const found = risks.value.findIndex(r => r.id === matched.id)
      riskIdx = found >= 0 ? String(found + 1) : undefined
    }
    return { text, risk, riskId, riskIdx, isSection }
  })
})

const groupedRisks = computed(() => {
  const groups: Record<string, any[]> = {}
  const order = ['支付条款', '违约责任', '争议解决', '质量验收', '知识产权', '权利义务', '其他']
  risks.value.forEach(r => {
    if (!groups[r.category]) groups[r.category] = []
    groups[r.category].push(r)
  })
  const sorted: Record<string, any[]> = {}
  order.forEach(c => { if (groups[c]) sorted[c] = groups[c] })
  Object.keys(groups).forEach(c => { if (!sorted[c]) sorted[c] = groups[c] })
  return sorted
})

const highCount = computed(() => risks.value.filter(r => r.risk_level === 'high').length)
const mediumCount = computed(() => risks.value.filter(r => r.risk_level === 'medium').length)

async function fetchRisks() {
  try {
    const res = await riskApi.list(Number(route.params.id))
    // Attach 1-based index for cross-reference numbering
    risks.value = res.data.map((r: any, i: number) => ({ ...r, _idx: i + 1 }))
  } catch {
    msg.error('加载风险列表失败')
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

function quickQuestion(text: string) {
  chatInput.value = text
  sendChat()
}

async function sendChat() {
  if (!chatInput.value) return
  const text = chatInput.value
  chatMessages.value.push({ role: 'user', content: text })
  chatInput.value = ''
  sendingChat.value = true
  scrollMessages()
  try {
    const res = await api.post(`/contracts/${route.params.id}/chat`, { message: text })
    chatMessages.value.push({ role: 'assistant', content: res.data.content })
    scrollMessages()
  } catch {
    chatMessages.value.push({ role: 'assistant', content: '发送失败，请重试' })
    scrollMessages()
  } finally {
    sendingChat.value = false
  }
}

function scrollMessages() {
  setTimeout(() => {
    if (msgListRef.value) {
      msgListRef.value.scrollTop = msgListRef.value.scrollHeight
    }
  }, 50)
}

async function scrollToRisk(id: number) {
  highlightedId.value = id
  await nextTick()
  const el = riskBodyRef.value?.querySelector(`[data-risk-id="${id}"]`)
  if (el) {
    el.scrollIntoView({ block: 'start', behavior: 'smooth' })
    // Clear highlight after animation
    setTimeout(() => { highlightedId.value = null }, 2000)
  }
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

<style scoped>
.loading-state {
  text-align: center;
  padding: 80px;
  color: #999;
}
.loading-state p {
  margin-top: 16px;
}

.workbench {
  display: flex;
  height: calc(100vh - 56px);
  background: #f5f5f5;
}

/* Left panel */
.left-panel {
  flex: 1;
  overflow-y: auto;
  padding: 24px 32px;
  border-right: 1px solid #e0e0e0;
}

.contract-doc {
  background: #fff;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.06);
  padding: 40px 48px;
  max-width: 820px;
  margin: 0 auto;
  font-size: 14px;
  line-height: 2;
  color: #222;
}

.doc-title {
  text-align: center;
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 28px;
  letter-spacing: 3px;
}

.doc-body {
  border-top: 1px solid #eee;
  padding-top: 20px;
}

.doc-line {
  padding: 2px 0;
  position: relative;
  display: flex;
  align-items: baseline;
  gap: 6px;
}

.doc-line.is-empty {
  height: 0.5em;
}

.doc-line.section-title .line-text {
  font-weight: 700;
  font-size: 15px;
  margin-top: 6px;
  display: block;
}

.doc-line.has-risk {
  cursor: pointer;
  border-radius: 3px;
  background: rgba(239,68,68,0.06);
  transition: background 0.15s;
}
.doc-line.has-risk:hover {
  background: rgba(239,68,68,0.12);
}

/* Risk number tag (shared left + right) */
.risk-tag {
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  font-size: 11px;
  font-weight: 700;
  color: #fff;
}
.tag-high { background: #ef4444; }
.tag-medium { background: #f59e0b; }
.tag-low { background: #3b82f6; }

.line-text {
  flex: 1;
}

.empty-state {
  text-align: center;
  color: #999;
  padding: 60px 0;
}

/* Right panel */
.right-panel {
  width: 420px;
  display: flex;
  flex-direction: column;
  background: #fff;
}

.panel-header {
  padding: 14px 16px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-shrink: 0;
}

.panel-title {
  font-weight: 700;
  font-size: 15px;
}

.count-group {
  display: flex;
  gap: 6px;
}

.count {
  font-size: 11px;
  font-weight: 600;
  padding: 2px 10px;
  border-radius: 10px;
}
.count.high { background: #fef2f2; color: #dc2626; }
.count.medium { background: #fffbeb; color: #d97706; }

.panel-body {
  flex: 1;
  overflow-y: auto;
  padding: 12px 16px;
  scroll-behavior: smooth;
}

.empty-hint {
  text-align: center;
  color: #999;
  padding: 60px 0;
  font-size: 13px;
}

.risk-group {
  margin-bottom: 20px;
}

.group-label {
  font-size: 12px;
  font-weight: 600;
  color: #888;
  margin-bottom: 8px;
  padding-left: 2px;
  letter-spacing: 0.5px;
}

/* Risk item card */
.risk-item {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  margin-bottom: 10px;
  overflow: hidden;
  transition: box-shadow 0.15s, background 0.3s;
}
.risk-item:hover { box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
.risk-item.level-high { border-left: 3px solid #ef4444; }
.risk-item.level-medium { border-left: 3px solid #f59e0b; }
.risk-item.level-low { border-left: 3px solid #3b82f6; }

/* Highlight animation when scrolled to from left */
.risk-item.risk-highlighted {
  background: #fef3c7;
  box-shadow: 0 0 0 2px #f59e0b;
}

.item-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: #f9fafb;
  border-bottom: 1px solid #f0f0f0;
}

.item-pos {
  font-size: 11px;
  color: #999;
}

.item-status {
  margin-left: auto;
  font-size: 11px;
  padding: 1px 8px;
  border-radius: 4px;
  font-weight: 500;
}
.item-status.fixed { background: #d1fae5; color: #065f46; }
.item-status.ignored { background: #f3f4f6; color: #9ca3af; }

.item-desc {
  font-size: 13px;
  line-height: 1.6;
  color: #333;
  padding: 10px 12px 6px;
}
.level-high .item-desc { color: #991b1b; }
.level-medium .item-desc { color: #92400e; }

.item-suggestion {
  font-size: 12px;
  color: #166534;
  padding: 6px 12px;
  background: #f0fdf4;
  margin: 0 12px 6px;
  border-radius: 6px;
  line-height: 1.5;
}

.item-law {
  font-size: 12px;
  color: #1e40af;
  padding: 0 12px 6px;
  line-height: 1.5;
}

.item-actions {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
  padding: 8px 12px;
  border-top: 1px solid #f0f0f0;
  background: #fafafa;
}

/* Robot icon */
.robot-btn {
  position: fixed;
  bottom: 32px;
  right: 32px;
  width: 52px;
  height: 52px;
  border-radius: 50%;
  background: #4f46e5;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 4px 16px rgba(79,70,229,0.4);
  transition: transform 0.2s, box-shadow 0.2s;
  z-index: 100;
}
.robot-btn:hover {
  transform: scale(1.08);
  box-shadow: 0 6px 24px rgba(79,70,229,0.5);
}

/* Chat overlay & panel */
.chat-overlay {
  position: fixed;
  inset: 0;
  z-index: 200;
  background: rgba(0,0,0,0.12);
}
.chat-panel {
  position: absolute;
  top: 0;
  right: 0;
  width: 400px;
  height: 100%;
  background: #fff;
  display: flex;
  flex-direction: column;
  box-shadow: -8px 0 32px rgba(0,0,0,0.12);
}
.chat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  background: linear-gradient(135deg, #1e3a8a 0%, #4f46e5 100%);
  color: #fff;
  flex-shrink: 0;
}
.chat-header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}
.chat-header-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  background: rgba(255,255,255,0.15);
  border-radius: 10px;
}
.chat-title {
  font-weight: 700;
  font-size: 15px;
  line-height: 1.3;
}
.chat-subtitle {
  font-size: 11px;
  opacity: 0.75;
  line-height: 1.3;
}
.chat-close-btn {
  color: rgba(255,255,255,0.8) !important;
  transition: color 0.15s;
}
.chat-close-btn:hover {
  color: #fff !important;
}
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: #f8f9fb;
}

/* Welcome screen */
.chat-welcome {
  text-align: center;
  padding: 32px 16px;
}
.welcome-icon {
  color: #4f46e5;
  opacity: 0.6;
  margin-bottom: 12px;
}
.welcome-text {
  font-size: 15px;
  font-weight: 600;
  color: #1e3a8a;
  margin-bottom: 8px;
}
.welcome-hint {
  font-size: 12px;
  color: #999;
  margin-bottom: 20px;
  line-height: 1.5;
}
.welcome-suggestions {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.suggestion-tag {
  display: block;
  padding: 10px 14px;
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 12px;
  color: #4f46e5;
  cursor: pointer;
  transition: all 0.15s;
  line-height: 1.4;
}
.suggestion-tag:hover {
  border-color: #4f46e5;
  background: #f5f3ff;
  box-shadow: 0 2px 8px rgba(79,70,229,0.1);
}

/* Messages */
.msg {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}
.msg-avatar {
  flex-shrink: 0;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 2px;
}
.msg-user .msg-avatar {
  background: #e0e7ff;
  color: #4338ca;
  order: 1;
}
.msg-assistant .msg-avatar {
  background: #4f46e5;
  color: #fff;
}
.msg-body {
  flex: 1;
  min-width: 0;
}
.msg-user .msg-body {
  text-align: right;
}
.msg-label {
  font-size: 11px;
  color: #999;
  margin-bottom: 4px;
}
.msg-content {
  display: inline-block;
  font-size: 13px;
  line-height: 1.6;
  padding: 10px 14px;
  border-radius: 12px;
  text-align: left;
  word-break: break-word;
}
.msg-user .msg-content {
  background: #4f46e5;
  color: #fff;
  border-bottom-right-radius: 4px;
}
.msg-assistant .msg-content {
  display: block;
  background: #fff;
  color: #333;
  border: 1px solid #e5e7eb;
  border-bottom-left-radius: 4px;
}
.msg-assistant .msg-content :deep(p) {
  margin: 6px 0;
  line-height: 1.7;
}
.msg-assistant .msg-content :deep(p:first-child) {
  margin-top: 0;
}
.msg-assistant .msg-content :deep(p:last-child) {
  margin-bottom: 0;
}
.msg-assistant .msg-content :deep(ul),
.msg-assistant .msg-content :deep(ol) {
  margin: 4px 0;
  padding-left: 20px;
}
.msg-assistant .msg-content :deep(li) {
  margin: 3px 0;
  line-height: 1.6;
}
.msg-assistant .msg-content :deep(strong) {
  font-weight: 700;
  color: #111;
}
.msg-assistant .msg-content :deep(code) {
  background: #f3f4f6;
  padding: 1px 5px;
  border-radius: 3px;
  font-size: 12px;
  color: #dc2626;
}
.msg-assistant .msg-content :deep(pre) {
  background: #f8f9fb;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  padding: 12px;
  overflow-x: auto;
  margin: 8px 0;
}
.msg-assistant .msg-content :deep(pre code) {
  background: none;
  padding: 0;
  color: #333;
  font-size: 12px;
}
.msg-assistant .msg-content :deep(h1),
.msg-assistant .msg-content :deep(h2),
.msg-assistant .msg-content :deep(h3),
.msg-assistant .msg-content :deep(h4) {
  margin: 10px 0 4px;
  font-weight: 700;
  color: #1e3a8a;
}
.msg-assistant .msg-content :deep(hr) {
  border: none;
  border-top: 1px solid #e5e7eb;
  margin: 12px 0;
}
.msg-assistant .msg-content.thinking {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: #999;
  font-style: italic;
  border-color: #e5e7eb;
}
.dot-pulse {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #4f46e5;
  animation: dotPulse 1.2s ease-in-out infinite;
}
@keyframes dotPulse {
  0%, 80%, 100% { opacity: 0.3; transform: scale(0.8); }
  40% { opacity: 1; transform: scale(1); }
}

/* Input bar */
.chat-input-bar {
  padding: 12px 16px;
  border-top: 1px solid #e5e7eb;
  display: flex;
  gap: 8px;
  flex-shrink: 0;
  background: #fff;
}
.chat-input {
  --n-border: 1px solid #e5e7eb !important;
  --n-border-focus: 1px solid #4f46e5 !important;
  --n-box-shadow-focus: 0 0 0 2px rgba(79,70,229,0.1) !important;
}
.chat-send-btn {
  --n-color: #4f46e5 !important;
  --n-color-hover: #4338ca !important;
}

/* Slide transition */
.slide-enter-active,
.slide-leave-active {
  transition: opacity 0.2s;
}
.slide-enter-active .chat-panel,
.slide-leave-active .chat-panel {
  transition: transform 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}
.slide-enter-from { opacity: 0; }
.slide-enter-from .chat-panel { transform: translateX(100%); }
.slide-leave-to { opacity: 0; }
.slide-leave-to .chat-panel { transform: translateX(100%); }

</style>
