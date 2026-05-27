<template>
  <div style="min-height:100vh;background:#f4f7fa;">
    <n-layout>
      <n-layout-header style="background:#1e3a8a;padding:0 24px;display:flex;align-items:center;height:56px;color:#fff;">
        <div style="display:flex;align-items:center;gap:8px;font-size:18px;font-weight:bold;">
          <n-icon size="24" color="#93c5fd"><i class="fas fa-shield-alt"></i></n-icon>
          智审通 AI
        </div>
        <div style="flex:1;display:flex;gap:24px;margin-left:48px;font-size:14px;">
          <router-link to="/" style="color:#fff;text-decoration:none;opacity:0.85;">合同上传</router-link>
          <router-link to="/contracts" style="color:#fff;text-decoration:none;opacity:0.85;">审查记录</router-link>
          <router-link to="/templates" style="color:#fff;text-decoration:none;opacity:0.85;">模板库</router-link>
          <router-link v-if="auth.user?.role==='admin'" to="/admin" style="color:#fff;text-decoration:none;opacity:0.85;">管理</router-link>
        </div>
        <div style="margin-left:auto;display:flex;align-items:center;gap:12px;font-size:13px;">
          <span style="opacity:0.9;">{{ auth.user?.display_name }} ({{ auth.user?.department }})</span>
          <n-button size="small" quaternary style="color:#fff;" @click="auth.logout()">退出</n-button>
        </div>
      </n-layout-header>
      <n-layout-content style="padding:24px;max-width:1200px;margin:0 auto;width:100%;">
        <slot />
      </n-layout-content>
    </n-layout>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '../stores/auth'
const auth = useAuthStore()
</script>
