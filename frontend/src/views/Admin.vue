<template>
  <div>
    <h2 style="font-size:20px;margin-bottom:24px;">管理面板</h2>
    <div v-if="loading" style="text-align:center;padding:40px;"><n-spin size="large" /></div>
    <div v-else>
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-bottom:32px;">
        <div style="background:#fff;border-radius:12px;padding:24px;border:1px solid #eee;">
          <p style="font-size:12px;color:#999;">审查总数</p>
          <p style="font-size:32px;font-weight:bold;">{{ stats.total_contracts }}</p>
        </div>
        <div style="background:#fff;border-radius:12px;padding:24px;border:1px solid #fecaca;border-left:4px solid #dc2626;">
          <p style="font-size:12px;color:#999;">高风险合同</p>
          <p style="font-size:32px;font-weight:bold;color:#dc2626;">{{ stats.high_risk }}</p>
        </div>
        <div style="background:#fff;border-radius:12px;padding:24px;border:1px solid #dbeafe;border-left:4px solid #2563eb;">
          <p style="font-size:12px;color:#999;">平均合规分</p>
          <p style="font-size:32px;font-weight:bold;color:#2563eb;">{{ stats.avg_score }}</p>
        </div>
      </div>
      <div style="background:#fff;border-radius:12px;padding:24px;border:1px solid #eee;">
        <h3 style="font-size:16px;margin-bottom:16px;">用户列表</h3>
        <n-table :bordered="false">
          <thead>
            <tr><th>用户名</th><th>姓名</th><th>角色</th><th>部门</th></tr>
          </thead>
          <tbody>
            <tr v-for="u in users" :key="u.id">
              <td>{{ u.username }}</td>
              <td>{{ u.display_name }}</td>
              <td><n-tag size="small" :color="u.role === 'admin' ? '#1e3a8a' : '#6b7280'">{{ u.role }}</n-tag></td>
              <td>{{ u.department }}</td>
            </tr>
          </tbody>
        </n-table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '../api/request'

const stats = ref({ total_contracts: 0, high_risk: 0, avg_score: 0 })
const users = ref<any[]>([])
const loading = ref(true)

onMounted(async () => {
  try {
    const [s, u] = await Promise.all([
      api.get('/admin/stats'),
      api.get('/admin/users'),
    ])
    stats.value = s.data
    users.value = u.data
  } catch { /* ignore */ } finally {
    loading.value = false
  }
})
</script>
