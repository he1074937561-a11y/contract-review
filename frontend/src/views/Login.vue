<template>
  <div style="min-height:100vh;display:flex;align-items:center;justify-content:center;background:#f0f4f8;">
    <div style="display:flex;width:900px;height:500px;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 20px 60px rgba(0,0,0,0.1);">
      <div style="width:50%;background:#1e3a8a;padding:40px;color:#fff;display:flex;flex-direction:column;justify-content:space-between;">
        <div>
          <div style="font-size:24px;font-weight:bold;">智审通 AI</div>
          <h1 style="font-size:28px;margin-top:32px;line-height:1.3;">专业、严谨、高效的<br/>AI 合同审查平台</h1>
          <p style="margin-top:12px;opacity:0.8;">基于 LLM 技术，深度识别合同条款风险</p>
        </div>
        <div style="display:flex;flex-direction:column;gap:12px;">
          <div style="display:flex;align-items:center;gap:8px;"><span style="color:#22c55e;">✓</span> 精准解析合同文本</div>
          <div style="display:flex;align-items:center;gap:8px;"><span style="color:#22c55e;">✓</span> 多维风险条款高亮</div>
          <div style="display:flex;align-items:center;gap:8px;"><span style="color:#22c55e;">✓</span> 一键生成专业审查报告</div>
        </div>
      </div>
      <div style="width:50%;padding:48px;display:flex;flex-direction:column;justify-content:center;">
        <h2 style="margin-bottom:4px;">欢迎回来</h2>
        <p style="color:#999;margin-bottom:24px;">请输入账号密码登录系统</p>
        <n-form @submit.prevent="handleLogin">
          <n-input v-model:value="username" placeholder="账号" size="large" style="margin-bottom:16px;" />
          <n-input v-model:value="password" type="password" placeholder="密码" size="large" style="margin-bottom:24px;" show-password-on="click" />
          <n-button type="primary" size="large" block :loading="loading" attr-type="submit">进入系统</n-button>
        </n-form>
        <p style="margin-top:24px;text-align:center;font-size:12px;color:#ccc;">© 2026 AI 合同审查系统</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useMessage } from 'naive-ui'

const router = useRouter()
const auth = useAuthStore()
const msg = useMessage()
const username = ref('')
const password = ref('')
const loading = ref(false)

async function handleLogin() {
  loading.value = true
  try {
    await auth.login(username.value, password.value)
    router.push('/')
  } catch {
    msg.error('登录失败，请检查账号密码')
  } finally {
    loading.value = false
  }
}
</script>
