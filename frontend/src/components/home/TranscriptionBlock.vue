<script setup lang="ts">
import { onBeforeUnmount, ref } from 'vue'
import { ChevronDown, Copy, Languages, Sparkles } from 'lucide-vue-next'

const label = 'Транскрипция'
const buttonLabel = 'Переведено'
const text =
  'SPF скатывается? Смотри — вот эти катышки. И нет, это не всегда «плохой SPF».\\n\\nСкатывается по трём причинам: первая — ты намазал под SPF слишком много всего.\\n'

const isAdapting = ref(false)
let adaptTimer: ReturnType<typeof setTimeout> | null = null

function runAdaptAnimation() {
  if (isAdapting.value) return
  isAdapting.value = true
  if (adaptTimer) clearTimeout(adaptTimer)
  adaptTimer = setTimeout(() => {
    isAdapting.value = false
    adaptTimer = null
  }, 2000)
}

onBeforeUnmount(() => {
  if (adaptTimer) clearTimeout(adaptTimer)
})
</script>

<template>
  <section class="block">
    <div class="block__header">
      <div class="block__title">{{ label }}</div>
      <div class="block__actions">
        <button class="block__secondaryBtn" type="button">
          <span class="block__secondaryIcon" aria-hidden="true">
            <Languages :size="14" :stroke-width="2.2" color="#2B31B3" />
          </span>
          {{ buttonLabel }}
        </button>
        <button class="block__copyBtn" type="button" aria-label="Скопировать">
          <Copy :size="16" :stroke-width="2.2" color="#3A4951" />
        </button>
      </div>
    </div>

    <div class="block__content">
      <div class="block__text">{{ text }}</div>
      <button class="block__more" type="button">
        <ChevronDown :size="14" :stroke-width="2.2" /> Ещё
      </button>
    </div>

    <button class="block__primaryBtn" :class="{ 'block__primaryBtn--loading': isAdapting }" type="button" @click="runAdaptAnimation">
      <span class="block__primaryLabel" :class="{ 'block__primaryLabel--hidden': isAdapting }">
        <Sparkles :size="18" :stroke-width="2.2" />
        Адаптировать
      </span>
      <span class="block__primaryLoading" :class="{ 'block__primaryLoading--visible': isAdapting }">
        <span class="block__primarySpinner" />
        Адаптируем...
      </span>
    </button>
  </section>
</template>

<style scoped>
.block {
  width: 100%;
  max-width: 624px;
  min-height: 257px;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  gap: 10px;
}

.block__header {
  width: 100%;
  height: 32px;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
}

.block__actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.block__title {
  width: auto;
  flex: 1;
  min-width: 0;
  font-family: var(--heading);
  font-weight: 600;
  font-size: 16px;
  line-height: 24px;
  letter-spacing: 0.15px;
  color: #111827;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.block__secondaryBtn {
  min-width: 128px;
  height: 32px;
  background: #eef2ff;
  border: 1px solid rgba(43, 49, 179, 0.18);
  border-radius: 12px;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  gap: 4px;
  cursor: pointer;
  padding: 0 10px;
  color: #2b31b3;
  font-family: var(--heading);
  font-weight: 600;
  font-size: 12px;
  line-height: 16px;
  letter-spacing: 0.3px;
  transition: background-color 0.18s ease, border-color 0.18s ease, color 0.18s ease;
}

.block__secondaryBtn:hover {
  background: #e1e8ff;
  border-color: rgba(43, 49, 179, 0.28);
}

.block__secondaryBtn:focus-visible {
  outline: 3px solid rgba(43, 49, 179, 0.25);
  outline-offset: 2px;
}

.block__secondaryIcon {
  width: 16px;
  height: 16px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
}

.block__content {
  width: 100%;
  min-height: 217px;
  background: #f8fafc;
  border: 1px solid rgba(16, 24, 40, 0.08);
  border-radius: 14px;
  padding: 16px 16px 12px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.block__text {
  width: 100%;
  height: 149px;
  font-family: var(--sans);
  font-weight: 400;
  font-size: 14px;
  line-height: 21px;
  letter-spacing: 0.25px;
  color: #344054;
  white-space: pre-wrap;
  overflow: hidden;
}

.block__more {
  width: 76px;
  height: 32px;
  border-radius: 12px;
  border: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  background: #eef2f7;
  color: #1f2937;
  font-family: var(--heading);
  font-weight: 600;
  font-size: 12px;
  line-height: 16px;
  letter-spacing: 0.4px;
  cursor: pointer;
  margin-left: auto;
}

.block__primaryBtn {
  width: 220px;
  height: 56px;
  background: #2b31b3;
  border-radius: 12px;
  border: 0;
  cursor: pointer;
  color: #ffffff;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-family: var(--heading);
  font-weight: 700;
  font-size: 16px;
  line-height: 24px;
  letter-spacing: 0.5px;
  box-shadow: 0 10px 18px rgba(43, 49, 179, 0.24);
  transition: background-color 0.18s ease, transform 0.18s ease;
  position: relative;
  overflow: hidden;
}

.block__copyBtn {
  width: 32px;
  height: 32px;
  border: 0;
  border-radius: 12px;
  background: #f4f5f6;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.block__primaryBtn:hover {
  background: #242aa0;
  transform: translateY(-1px);
}

.block__primaryBtn--loading {
  background: #242aa0;
}

.block__primaryLabel {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  opacity: 1;
  transition: opacity 0.2s ease;
}

.block__primaryLabel--hidden {
  opacity: 0;
}

.block__primaryLoading {
  position: absolute;
  inset: 0;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  opacity: 0;
  transition: opacity 0.22s ease;
  pointer-events: none;
}

.block__primaryLoading--visible {
  opacity: 1;
}

.block__primarySpinner {
  width: 16px;
  height: 16px;
  border-radius: 999px;
  border: 2px solid rgba(255, 255, 255, 0.35);
  border-top-color: #ffffff;
  animation: spin 0.75s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>

