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
import { useAuthStore } from './stores/auth'

const auth = useAuthStore()
onMounted(async () => {
  if (auth.token) {
    try { await auth.fetchMe() } catch { auth.logout() }
  }
})
</script>
