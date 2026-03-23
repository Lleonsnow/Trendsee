<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const title = computed(() => {
  const raw = route.query.title
  return typeof raw === 'string' && raw.trim().length > 0 ? raw : 'Заглушка'
})

function goBack() {
  if (window.history.length > 1) {
    router.back()
    return
  }

  void router.push({ name: 'main' })
}
</script>

<template>
  <main class="stub">
    <section class="stub__card">
      <span class="stub__badge">Скоро</span>
      <h1 class="stub__title">{{ title }}</h1>
      <p class="stub__text">
        Раздел находится в разработке. Структура готова, скоро добавим контент и рабочие сценарии.
      </p>

      <button type="button" class="stub__back" @click="goBack">Назад</button>
    </section>
  </main>
</template>

<style scoped>
.stub {
  min-height: 100svh;
  padding: 40px 16px;
  box-sizing: border-box;
  display: grid;
  place-items: center;
  background:
    radial-gradient(120% 90% at 10% 0%, rgba(43, 49, 179, 0.12) 0%, rgba(43, 49, 179, 0) 55%),
    radial-gradient(120% 90% at 100% 100%, rgba(111, 70, 255, 0.12) 0%, rgba(111, 70, 255, 0) 50%),
    #f4f5f6;
}

.stub__card {
  width: min(560px, 100%);
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(16, 24, 40, 0.08);
  box-shadow: 0 18px 40px rgba(16, 24, 40, 0.08);
  backdrop-filter: blur(8px);
  padding: 28px;
  box-sizing: border-box;
}

.stub__badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 28px;
  padding: 0 12px;
  border-radius: 999px;
  background: rgba(43, 49, 179, 0.12);
  color: #2b31b3;
  font-family: var(--heading);
  font-weight: 600;
  font-size: 13px;
  line-height: 18px;
  margin-bottom: 14px;
}

.stub__title {
  margin: 0 0 10px;
  font-family: var(--heading);
  font-weight: 700;
  font-size: 34px;
  line-height: 1.15;
  letter-spacing: -0.03em;
  color: #101828;
}

.stub__text {
  margin: 0;
  max-width: 48ch;
  color: #4e616b;
  font-size: 16px;
  line-height: 1.55;
}

.stub__back {
  margin-top: 22px;
  border: 0;
  border-radius: 12px;
  background: #2b31b3;
  color: #ffffff;
  text-decoration: none;
  font-weight: 600;
  font-size: 14px;
  line-height: 21px;
  padding: 10px 16px;
  cursor: pointer;
  transition: transform 0.15s ease, box-shadow 0.15s ease, background-color 0.15s ease;
}

.stub__back:hover {
  background: #242aa0;
  transform: translateY(-1px);
  box-shadow: 0 10px 20px rgba(43, 49, 179, 0.22);
}

.stub__back:active {
  transform: translateY(0);
}

.stub__back:focus-visible {
  outline: 3px solid rgba(43, 49, 179, 0.28);
  outline-offset: 2px;
}
</style>

