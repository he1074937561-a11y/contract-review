<template>
  <n-loading-bar-provider>
    <n-message-provider>
      <n-dialog-provider>
        <router-view />
      </n-dialog-provider>
    </n-message-provider>
  </n-loading-bar-provider>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from './stores/auth'

const auth = useAuthStore()
const router = useRouter()

onMounted(async () => {
  if (auth.token) {
    try {
      await auth.fetchMe()
    } catch {
      auth.logout()
      router.push('/login')
    }
  }
})
</script>
