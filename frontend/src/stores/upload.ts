import { reactive } from 'vue'

export const pendingUpload = reactive<{
  file: File | null
  title: string
}>({
  file: null,
  title: '',
})
