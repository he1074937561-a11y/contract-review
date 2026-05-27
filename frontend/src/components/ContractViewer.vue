<template>
  <div style="background:#fff;padding:32px;border-radius:8px;box-shadow:0 1px 4px rgba(0,0,0,0.06);font-size:14px;line-height:1.8;max-width:800px;margin:0 auto;">
    <h2 style="text-align:center;font-size:20px;margin-bottom:24px;">{{ title }}</h2>
    <div v-for="(seg, i) in segments" :key="i" style="display:inline;">
      <span v-if="!seg.risk" v-html="seg.text"></span>
      <span v-else
        :style="{
          background: bgColor(seg.risk),
          borderBottom: `2px solid ${borderColor(seg.risk)}`,
          cursor: 'pointer',
          padding: '1px 0',
        }"
        @click="$emit('risk-click', seg.riskId)"
      >{{ seg.text }}</span>
    </div>
    <div v-if="!segments.length" style="color:#999;text-align:center;padding:40px;">暂无合同原文</div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  title: string
  segments: { text: string; risk?: string; riskId?: number }[]
}>()

defineEmits<{ (e: 'risk-click', id: number): void }>()

function bgColor(level: string) {
  return level === 'high' ? 'rgba(239,68,68,0.15)' : level === 'medium' ? 'rgba(245,158,11,0.15)' : 'rgba(59,130,246,0.15)'
}
function borderColor(level: string) {
  return level === 'high' ? '#ef4444' : level === 'medium' ? '#f59e0b' : '#3b82f6'
}
</script>
