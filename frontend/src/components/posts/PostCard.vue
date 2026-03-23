<script setup lang="ts">
import { computed } from 'vue'
import type { Post } from '../../types/posts'
import { formatRuDate } from '../../utils/date'

const props = defineProps<{
  post: Post
}>()

const emit = defineEmits<{
  (e: 'open', post: Post): void
}>()

const preview = computed(() => {
  const text = props.post.text ?? ''
  const maxLen = 140
  if (text.length <= maxLen) return text
  return `${text.slice(0, maxLen)}…`
})

function open() {
  emit('open', props.post)
}
</script>

<template>
  <article
    class="post-card"
    role="button"
    tabindex="0"
    @click="open"
    @keydown.enter.prevent="open"
    @keydown.space.prevent="open"
  >
    <div class="post-card__title">{{ post.title }}</div>
    <div class="post-card__text">{{ preview }}</div>
    <div class="post-card__date">{{ formatRuDate(post.created_at) }}</div>
  </article>
</template>

<style scoped>
.post-card {
  border: 1px solid var(--border, rgba(0, 0, 0, 0.12));
  border-radius: 14px;
  padding: 16px 16px 14px;
  background: color-mix(in oklab, var(--bg, #fff) 92%, var(--accent-bg, rgba(170, 59, 255, 0.08)));
  box-shadow: var(--shadow, rgba(0, 0, 0, 0.06) 0 6px 18px);
  cursor: pointer;
  transition: transform 0.15s ease, border-color 0.15s ease;
}

.post-card:hover {
  transform: translateY(-1px);
  border-color: color-mix(in oklab, var(--accent-border, rgba(170, 59, 255, 0.6)) 55%, transparent);
}

.post-card:focus-visible {
  outline: 2px solid var(--accent, #aa3bff);
  outline-offset: 2px;
}

.post-card__title {
  color: var(--text-h, #08060d);
  font-size: 18px;
  font-weight: 650;
  margin-bottom: 8px;
}

.post-card__text {
  color: var(--text, #6b6375);
  font-size: 15px;
  line-height: 1.4;
  margin-bottom: 12px;
  white-space: pre-wrap;
}

.post-card__date {
  font-size: 13px;
  color: color-mix(in oklab, var(--text, #6b6375) 85%, #000 15%);
}
</style>

