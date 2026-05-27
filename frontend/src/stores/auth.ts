import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../api/request'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<any>(null)
  const token = ref(localStorage.getItem('token') || '')

  async function login(username: string, password: string) {
    const res = await api.post('/auth/login', { username, password })
    token.value = res.data.access_token
    user.value = res.data.user
    localStorage.setItem('token', token.value)
  }

  async function fetchMe() {
    const res = await api.get('/auth/me')
    user.value = res.data
  }

  function logout() {
    token.value = ''
    user.value = null
    localStorage.removeItem('token')
  }

  return { user, token, login, fetchMe, logout }
})
