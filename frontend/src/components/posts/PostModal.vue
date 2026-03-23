<script setup lang="ts">
import { onBeforeUnmount, onMounted } from 'vue'
import type { Post } from '../../types/posts'
import { formatRuDate } from '../../utils/date'

const props = defineProps<{
  post: Post
}>()

const emit = defineEmits<{
  (e: 'close'): void
}>()

function onKeyDown(e: KeyboardEvent) {
  if (e.key === 'Escape') emit('close')
}

onMounted(() => {
  window.addEventListener('keydown', onKeyDown)
})

onBeforeUnmount(() => {
  window.removeEventListener('keydown', onKeyDown)
})
</script>

<template>
  <div class="modal-overlay" @click.self="emit('close')" role="dialog" aria-modal="true">
    <div class="modal">
      <header class="modal__header">
        <h2 class="modal__title">{{ post.title }}</h2>
        <button class="modal__close" type="button" @click="emit('close')" aria-label="Закрыть">
          ×
        </button>
      </header>

      <div class="modal__meta">
        <div>user_id: {{ post.user_id }}</div>
        <div>created_at: {{ formatRuDate(post.created_at) }}</div>
        <div>updated_at: {{ formatRuDate(post.updated_at) }}</div>
      </div>

      <div class="modal__body">
        <div class="modal__text">{{ post.text }}</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(10, 9, 14, 0.58);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 18px;
  z-index: 50;
}

.modal {
  width: 860px;
  max-width: 100%;
  border-radius: 18px;
  background: var(--bg, #fff);
  border: 1px solid var(--border, rgba(0, 0, 0, 0.12));
  box-shadow:
    rgba(0, 0, 0, 0.18) 0 30px 90px,
    rgba(0, 0, 0, 0.08) 0 10px 30px;
  overflow: hidden;
}

.modal__header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  padding: 16px 16px 10px;
  border-bottom: 1px solid var(--border, rgba(0, 0, 0, 0.12));
}

.modal__title {
  margin: 0;
  font-size: 22px;
  font-weight: 700;
  color: var(--text-h, #08060d);
}

.modal__close {
  border: 1px solid var(--border, rgba(0, 0, 0, 0.12));
  background: transparent;
  border-radius: 10px;
  width: 40px;
  height: 40px;
  font-size: 26px;
  line-height: 1;
  color: var(--text-h, #08060d);
  cursor: pointer;
  padding: 0;
}

.modal__close:focus-visible {
  outline: 2px solid var(--accent, #aa3bff);
  outline-offset: 2px;
}

.modal__meta {
  padding: 12px 16px;
  color: var(--text, #6b6375);
  font-size: 13px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px 14px;
}

.modal__body {
  padding: 8px 16px 18px;
}

.modal__text {
  white-space: pre-wrap;
  line-height: 1.5;
  color: var(--text, #6b6375);
  font-size: 15px;
}
</style>

