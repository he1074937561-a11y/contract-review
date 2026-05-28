<template>
  <div>
    <!-- Tabs -->
    <n-tabs v-model:value="activeTab" type="line" animated>
      <n-tab-pane name="dashboard" tab="仪表盘">
        <div v-if="loading.stats" style="text-align:center;padding:60px;"><n-spin size="large" /></div>
        <div v-else>
          <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:24px;">
            <div style="background:#fff;border-radius:12px;padding:20px 24px;border:1px solid #e5e7eb;display:flex;align-items:center;gap:16px;">
              <div style="width:44px;height:44px;background:#eef2ff;border-radius:12px;display:flex;align-items:center;justify-content:center;">
                <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="#4f46e5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
              </div>
              <div><p style="font-size:12px;color:#94a3b8;margin:0;">审查总数</p><p style="font-size:28px;font-weight:700;color:#1e293b;margin:2px 0 0;">{{ stats.total_contracts }}</p></div>
            </div>
            <div style="background:#fff;border-radius:12px;padding:20px 24px;border:1px solid #fecaca;display:flex;align-items:center;gap:16px;">
              <div style="width:44px;height:44px;background:#fef2f2;border-radius:12px;display:flex;align-items:center;justify-content:center;">
                <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="#dc2626" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
              </div>
              <div><p style="font-size:12px;color:#94a3b8;margin:0;">高风险合同</p><p style="font-size:28px;font-weight:700;color:#dc2626;margin:2px 0 0;">{{ stats.high_risk }}</p></div>
            </div>
            <div style="background:#fff;border-radius:12px;padding:20px 24px;border:1px solid #dbeafe;display:flex;align-items:center;gap:16px;">
              <div style="width:44px;height:44px;background:#eff6ff;border-radius:12px;display:flex;align-items:center;justify-content:center;">
                <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="#2563eb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
              </div>
              <div><p style="font-size:12px;color:#94a3b8;margin:0;">平均合规分</p><p style="font-size:28px;font-weight:700;color:#2563eb;margin:2px 0 0;">{{ stats.avg_score }}</p></div>
            </div>
            <div style="background:#fff;border-radius:12px;padding:20px 24px;border:1px solid #e5e7eb;display:flex;align-items:center;gap:16px;">
              <div style="width:44px;height:44px;background:#f0fdf4;border-radius:12px;display:flex;align-items:center;justify-content:center;">
                <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="#16a34a" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
              </div>
              <div><p style="font-size:12px;color:#94a3b8;margin:0;">用户总数</p><p style="font-size:28px;font-weight:700;color:#16a34a;margin:2px 0 0;">{{ stats.total_users }}</p></div>
            </div>
          </div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
            <div style="background:#fff;border-radius:12px;padding:20px;border:1px solid #e5e7eb;">
              <h3 style="font-size:14px;font-weight:600;margin:0 0 16px;color:#1e293b;">合同状态分布</h3>
              <div style="display:flex;gap:20px;">
                <div v-for="s in statusList" :key="s.key" style="flex:1;text-align:center;">
                  <div :style="{width:'40px',height:'40px',borderRadius:'10px',margin:'0 auto 6px',display:'flex',alignItems:'center',justifyContent:'center',background:s.bg,color:s.color}">
                    <span style="font-weight:700;font-size:16px;">{{ stats.contracts_by_status?.[s.key] ?? 0 }}</span>
                  </div>
                  <p style="font-size:11px;color:#94a3b8;margin:0;">{{ s.label }}</p>
                </div>
              </div>
            </div>
            <div style="background:#fff;border-radius:12px;padding:20px;border:1px solid #e5e7eb;">
              <h3 style="font-size:14px;font-weight:600;margin:0 0 16px;color:#1e293b;">今日上传</h3>
              <p style="font-size:36px;font-weight:700;color:#4f46e5;margin:0;">{{ stats.recent_contracts }}</p>
              <p style="font-size:12px;color:#94a3b8;margin:4px 0 0;">份合同</p>
            </div>
          </div>
        </div>
      </n-tab-pane>

      <n-tab-pane name="users" tab="用户管理">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;">
          <p style="font-size:13px;color:#94a3b8;margin:0;">共 {{ users.length }} 人</p>
          <n-button size="small" type="primary" @click="openCreateUser">新建用户</n-button>
        </div>
        <div v-if="loading.users" style="text-align:center;padding:40px;"><n-spin size="large" /></div>
        <div v-else style="background:#fff;border-radius:12px;border:1px solid #e5e7eb;overflow:hidden;">
          <n-table :bordered="false" :single-line="false">
            <thead><tr style="background:#f8fafc;">
              <th style="color:#64748b;font-weight:600;">用户名</th>
              <th style="color:#64748b;font-weight:600;">姓名</th>
              <th style="color:#64748b;font-weight:600;">角色</th>
              <th style="color:#64748b;font-weight:600;">部门</th>
              <th style="color:#64748b;font-weight:600;">状态</th>
              <th style="color:#64748b;font-weight:600;text-align:right;">操作</th>
            </tr></thead>
            <tbody>
              <tr v-for="u in users" :key="u.id" style="transition:background 0.15s;" @mouseenter="(e:any)=>e.currentTarget.style.background='#f8fafc'" @mouseleave="(e:any)=>e.currentTarget.style.background=''">
                <td style="font-weight:600;color:#1e293b;">{{ u.username }}</td>
                <td>{{ u.display_name }}</td>
                <td>
                  <span :style="{display:'inline-flex',alignItems:'center',gap:'4px',background:u.role==='admin'?'#1e3a8a':'#f1f5f9',color:u.role==='admin'?'#fff':'#64748b',fontSize:'11px',padding:'2px 10px',borderRadius:'10px',fontWeight:'500'}">
                    <span :style="{width:'5px',height:'5px',borderRadius:'50%',background:u.role==='admin'?'#93c5fd':'#94a3b8'}"></span>{{ u.role === 'admin' ? '管理员' : '审核人' }}
                  </span>
                </td>
                <td style="color:#64748b;">{{ u.department || '-' }}</td>
                <td><n-switch :value="u.is_active" size="small" @update:value="() => toggleStatus(u)" :disabled="u.id === currentUserId" /></td>
                <td style="text-align:right;white-space:nowrap;">
                  <n-button size="tiny" quaternary @click="openEditUser(u)">编辑</n-button>
                  <n-button size="tiny" quaternary type="error" @click="openDeleteUser(u)" :disabled="u.id === currentUserId">删除</n-button>
                </td>
              </tr>
            </tbody>
          </n-table>
        </div>
      </n-tab-pane>

      <n-tab-pane name="logs" tab="操作日志">
        <div style="margin-bottom:16px;">
          <n-select v-model:value="logFilter" :options="logFilterOptions" clearable placeholder="操作类型筛选" style="width:200px;" @update:value="fetchLogs" />
        </div>
        <div v-if="loading.logs" style="text-align:center;padding:40px;"><n-spin size="large" /></div>
        <div v-else style="background:#fff;border-radius:12px;border:1px solid #e5e7eb;overflow:hidden;">
          <n-table :bordered="false" :single-line="false">
            <thead><tr style="background:#f8fafc;">
              <th style="color:#64748b;font-weight:600;">时间</th>
              <th style="color:#64748b;font-weight:600;">用户</th>
              <th style="color:#64748b;font-weight:600;">操作</th>
              <th style="color:#64748b;font-weight:600;">对象</th>
              <th style="color:#64748b;font-weight:600;">详情</th>
            </tr></thead>
            <tbody>
              <tr v-for="log in logs" :key="log.id" style="transition:background 0.15s;">
                <td style="color:#94a3b8;font-size:12px;">{{ log.created_at?.slice(0, 19).replace('T', ' ') }}</td>
                <td>{{ log.username }}</td>
                <td><n-tag size="small" :color="actionColor(log.action)">{{ actionLabel(log.action) }}</n-tag></td>
                <td style="font-size:12px;color:#64748b;">{{ log.target_type }}{{ log.target_id ? ' #' + log.target_id : '' }}</td>
                <td style="font-size:12px;color:#64748b;max-width:300px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{{ log.detail }}</td>
              </tr>
              <tr v-if="!logs.length"><td colspan="5" style="text-align:center;color:#999;padding:40px;">暂无操作日志</td></tr>
            </tbody>
          </n-table>
        </div>
        <div v-if="logTotal > 50" style="display:flex;justify-content:flex-end;margin-top:16px;">
          <n-pagination :page="logPage" :page-count="Math.ceil(logTotal/50)" @update:page="(p:number)=>{logPage=p;fetchLogs()}" />
        </div>
      </n-tab-pane>

      <n-tab-pane name="config" tab="系统配置">
        <div v-if="loading.config" style="text-align:center;padding:40px;"><n-spin size="large" /></div>
        <div v-else style="max-width:500px;background:#fff;border-radius:12px;padding:24px;border:1px solid #e5e7eb;">
          <n-form label-placement="left" label-width="120">
            <n-form-item label="API Key">
              <n-input v-model:value="configForm.llm_api_key" type="password" show-password-on="click" placeholder="输入 DeepSeek API Key" />
            </n-form-item>
            <n-form-item label="模型">
              <n-input v-model:value="configForm.llm_model" placeholder="deepseek-chat" />
            </n-form-item>
            <n-form-item label="Base URL">
              <n-input v-model:value="configForm.llm_base_url" placeholder="https://api.deepseek.com" />
            </n-form-item>
            <n-form-item>
              <n-button type="primary" :loading="savingConfig" @click="saveConfig">保存配置</n-button>
            </n-form-item>
          </n-form>
        </div>
      </n-tab-pane>
    </n-tabs>

    <!-- User Create/Edit Modal -->
    <n-modal v-model:show="showUserModal" preset="card" :title="editingUser ? '编辑用户' : '新建用户'" style="width:480px;" :mask-closable="false">
      <n-form label-placement="left" label-width="80">
        <n-form-item label="用户名"><n-input v-model:value="userForm.username" :disabled="!!editingUser" placeholder="登录账号" /></n-form-item>
        <n-form-item label="姓名"><n-input v-model:value="userForm.display_name" placeholder="显示名称" /></n-form-item>
        <n-form-item :label="editingUser ? '新密码' : '密码'"><n-input v-model:value="userForm.password" type="password" :placeholder="editingUser ? '留空不修改' : '登录密码'" /></n-form-item>
        <n-form-item label="角色">
          <n-select v-model:value="userForm.role" :options="[{label:'管理员',value:'admin'},{label:'审核人',value:'reviewer'}]" />
        </n-form-item>
        <n-form-item label="部门"><n-input v-model:value="userForm.department" placeholder="所属部门" /></n-form-item>
      </n-form>
      <template #action>
        <n-button size="small" @click="showUserModal = false">取消</n-button>
        <n-button size="small" type="primary" :loading="savingUser" @click="saveUser">保存</n-button>
      </template>
    </n-modal>

    <!-- Delete User Confirm -->
    <n-modal v-model:show="showDeleteModal" preset="dialog" :mask-closable="false">
      <template #header><span style="font-size:16px;">确定删除用户？</span></template>
      <p style="color:#999;font-size:13px;margin:0;">删除后不可恢复，该用户将无法登录系统。</p>
      <template #action>
        <n-button size="small" @click="showDeleteModal = false">取消</n-button>
        <n-button size="small" type="error" :loading="deletingUser" @click="confirmDeleteUser">删除</n-button>
      </template>
    </n-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useMessage } from 'naive-ui'
import api from '../api/request'
import { useAuthStore } from '../stores/auth'

const msg = useMessage()
const auth = useAuthStore()
const currentUserId = auth.user?.id

const activeTab = ref('dashboard')

const loading = reactive({ stats: true, users: true, logs: true, config: true })

// ─── Dashboard ───
const stats = ref<any>({})
const statusList = [
  { key: 'completed', label: '已完成', bg: '#d1fae5', color: '#065f46' },
  { key: 'reviewing', label: '审查中', bg: '#dbeafe', color: '#1e40af' },
  { key: 'pending', label: '待处理', bg: '#fef3c7', color: '#92400e' },
  { key: 'failed', label: '失败', bg: '#fee2e2', color: '#991b1b' },
]

async function fetchStats() {
  loading.stats = true
  try {
    const res = await api.get('/admin/stats')
    stats.value = res.data
  } catch { msg.error('加载统计数据失败') }
  finally { loading.stats = false }
}

// ─── Users ───
const users = ref<any[]>([])
const showUserModal = ref(false)
const editingUser = ref<any>(null)
const savingUser = ref(false)
const userForm = ref({ username: '', display_name: '', password: '', role: 'reviewer', department: '' })
const showDeleteModal = ref(false)
const deletingUser = ref(false)
const deleteTarget = ref<any>(null)

async function fetchUsers() {
  loading.users = true
  try {
    const res = await api.get('/admin/users')
    users.value = res.data
  } catch { msg.error('加载用户列表失败') }
  finally { loading.users = false }
}

function openCreateUser() {
  editingUser.value = null
  userForm.value = { username: '', display_name: '', password: '', role: 'reviewer', department: '' }
  showUserModal.value = true
}

function openEditUser(u: any) {
  editingUser.value = u
  userForm.value = { username: u.username, display_name: u.display_name, password: '', role: u.role, department: u.department }
  showUserModal.value = true
}

async function saveUser() {
  if (!userForm.value.username || (!editingUser.value && !userForm.value.password)) {
    msg.warning('请填写必填项')
    return
  }
  savingUser.value = true
  try {
    if (editingUser.value) {
      const body: any = { display_name: userForm.value.display_name, role: userForm.value.role, department: userForm.value.department }
      if (userForm.value.password) body.password = userForm.value.password
      await api.put(`/admin/users/${editingUser.value.id}`, body)
      msg.success('已更新')
    } else {
      await api.post('/admin/users', userForm.value)
      msg.success('已创建')
    }
    showUserModal.value = false
    fetchUsers()
  } catch (e: any) {
    msg.error(e.response?.data?.detail || '操作失败')
  } finally {
    savingUser.value = false
  }
}

function openDeleteUser(u: any) {
  deleteTarget.value = u
  showDeleteModal.value = true
}

async function confirmDeleteUser() {
  if (!deleteTarget.value) return
  deletingUser.value = true
  try {
    await api.delete(`/admin/users/${deleteTarget.value.id}`)
    msg.success('已删除')
    showDeleteModal.value = false
    deleteTarget.value = null
    fetchUsers()
  } catch (e: any) {
    msg.error(e.response?.data?.detail || '删除失败')
  } finally {
    deletingUser.value = false
  }
}

async function toggleStatus(u: any) {
  try {
    const res = await api.put(`/admin/users/${u.id}/status`)
    u.is_active = res.data.is_active
    msg.success(u.is_active ? '已启用' : '已禁用')
  } catch (e: any) {
    msg.error(e.response?.data?.detail || '操作失败')
  }
}

// ─── Logs ───
const logs = ref<any[]>([])
const logFilter = ref('')
const logPage = ref(1)
const logTotal = ref(0)
const logFilterOptions = [
  { label: '创建', value: 'create' },
  { label: '编辑', value: 'update' },
  { label: '删除', value: 'delete' },
  { label: '启用/禁用', value: 'toggle_status' },
  { label: '风险更新', value: 'update_risk' },
  { label: '配置更新', value: 'update_config' },
]

function actionLabel(a: string) {
  const m: Record<string, string> = { create: '创建', update: '编辑', delete: '删除', toggle_status: '状态变更', upload: '上传', update_risk: '风险更新', update_config: '配置更新' }
  return m[a] || a
}
function actionColor(a: string) {
  const m: Record<string, string> = { create: '#16a34a', update: '#2563eb', delete: '#dc2626', toggle_status: '#d97706', upload: '#16a34a', update_risk: '#d97706', update_config: '#6b7280' }
  return m[a] || '#6b7280'
}

async function fetchLogs() {
  loading.logs = true
  try {
    const params: any = { page: logPage.value, page_size: 50 }
    if (logFilter.value) params.action = logFilter.value
    const res = await api.get('/admin/logs', { params })
    logs.value = res.data.items || []
    logTotal.value = res.data.total || 0
  } catch { msg.error('加载日志失败') }
  finally { loading.logs = false }
}

// ─── Config ───
const configForm = ref({ llm_api_key: '', llm_model: '', llm_base_url: '' })
const savingConfig = ref(false)

async function fetchConfig() {
  loading.config = true
  try {
    const res = await api.get('/admin/config')
    configForm.value = { llm_api_key: '', llm_model: res.data.llm_model || '', llm_base_url: res.data.llm_base_url || '' }
  } catch { msg.error('加载配置失败') }
  finally { loading.config = false }
}

async function saveConfig() {
  savingConfig.value = true
  try {
    const body: any = {}
    if (configForm.value.llm_api_key) body.llm_api_key = configForm.value.llm_api_key
    if (configForm.value.llm_model) body.llm_model = configForm.value.llm_model
    if (configForm.value.llm_base_url) body.llm_base_url = configForm.value.llm_base_url
    await api.put('/admin/config', body)
    msg.success('配置已保存')
  } catch { msg.error('保存失败') }
  finally { savingConfig.value = false }
}

// ─── Lifecycle ───
onMounted(() => {
  fetchStats()
  fetchUsers()
  fetchLogs()
  fetchConfig()
})
</script>
