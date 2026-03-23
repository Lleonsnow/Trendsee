<script setup lang="ts">
const title = 'Суть'
const essence =
  'Разбор состава/логики: он в человеческих словах переводит состав/механику (что реально делает «X», названия 2-3 работоспособных компонентов и 2-3 маркетинговых «пустых» обещания).'
</script>

<template>
  <section class="block">
    <div class="block__header">
      <div class="block__title">{{ title }}</div>
    </div>

    <div class="block__content">
      <div class="block__text">{{ essence }}</div>
    </div>
  </section>
</template>

<style scoped>
.block {
  width: 100%;
  max-width: 624px;
  height: 135px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.block__header {
  width: 100%;
  height: 32px;
  display: flex;
  align-items: center;
}

.block__title {
  width: auto;
  flex: 1;
  font-family: var(--heading);
  font-weight: 600;
  font-size: 16px;
  line-height: 24px;
  letter-spacing: 0.15px;
  color: #111827;
}

.block__content {
  width: 100%;
  height: 95px;
  background: #f8fafc;
  border-radius: 14px;
  border: 1px solid rgba(16, 24, 40, 0.08);
  padding: 16px;
  box-sizing: border-box;
  display: flex;
  align-items: flex-start;
}

.block__text {
  width: 100%;
  font-family: var(--sans);
  font-weight: 400;
  font-size: 14px;
  line-height: 21px;
  letter-spacing: 0.25px;
  color: #344054;
}
</style>

