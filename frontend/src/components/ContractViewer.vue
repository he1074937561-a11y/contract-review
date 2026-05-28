<template>
  <div class="contract-document">
    <h2 class="contract-title">{{ title }}</h2>
    <div class="contract-body">
      <div
        v-for="(seg, i) in segments"
        :key="i"
        :class="['contract-line', {
          'risk-highlight': seg.risk,
          'section-header': seg.isSection,
          'empty-line': !seg.text.trim(),
        }]"
        @click="seg.risk && $emit('risk-click', seg.riskId)"
      >
        <div v-if="seg.risk" class="risk-marker" :class="'risk-' + seg.risk" />
        <span class="line-text" :class="{ 'has-risk': seg.risk }">{{ seg.text }}</span>
      </div>
    </div>
    <div v-if="!segments.length" class="empty-state">暂无合同原文</div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  title: string
  segments: { text: string; risk?: string; riskId?: number; isSection?: boolean }[]
}>()

defineEmits<{ (e: 'risk-click', id: number): void }>()
</script>

<style scoped>
.contract-document {
  background: #fff;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.08);
  font-family: 'SimSun', 'STSong', 'Noto Serif CJK SC', serif;
  font-size: 14px;
  line-height: 1.9;
  max-width: 820px;
  margin: 0 auto;
  padding: 48px 56px;
  color: #1a1a1a;
}

.contract-title {
  text-align: center;
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 32px;
  letter-spacing: 4px;
  color: #000;
}

.contract-body {
  border-top: 1px solid #e5e7eb;
  padding-top: 24px;
}

.contract-line {
  position: relative;
  padding: 4px 0 4px 0;
  transition: background 0.15s;
}

.contract-line.risk-highlight {
  background: rgba(239,68,68,0.06);
  cursor: pointer;
  padding-left: 0;
}

.contract-line.empty-line {
  height: 0.6em;
}

.contract-line.section-header .line-text {
  font-weight: bold;
  font-size: 15px;
  color: #000;
  margin-top: 8px;
  display: block;
}

.risk-marker {
  position: absolute;
  left: -8px;
  top: 2px;
  bottom: 2px;
  width: 3px;
  border-radius: 2px;
}

.risk-marker.risk-high {
  background: #ef4444;
}

.risk-marker.risk-medium {
  background: #f59e0b;
}

.risk-marker.risk-low {
  background: #3b82f6;
}

.line-text.has-risk {
  border-bottom: 2px solid transparent;
}

.risk-highlight:hover .line-text.has-risk {
  border-bottom-color: #ef4444;
}

.empty-state {
  text-align: center;
  color: #999;
  padding: 60px 0;
}
</style>
