<script setup lang="ts">
import { ref } from 'vue'
import LeftNav from '../components/home/LeftNav.vue'
import RightSidebar from '../components/home/RightSidebar.vue'
import type { Post } from '../types/posts'

const selectedPost = ref<Post | null>(null)
</script>

<template>
  <div class="frame">
    <LeftNav />

    <section class="main">
      <RightSidebar :selectedPost="selectedPost" @select="selectedPost = $event" @clear="selectedPost = null" />
    </section>

    <button
      v-if="selectedPost"
      type="button"
      class="frame__dimmer"
      aria-label="Закрыть выбранный пост"
      @click="selectedPost = null"
    />
  </div>
</template>

<style scoped>
.frame {
  position: relative;
  width: 1280px;
  max-width: 100%;
  height: 950px;
  background: #f4f5f6;
  border-radius: 24px;
  overflow: hidden;
  display: flex;
  align-items: stretch;
  gap: 10px;
}

.main {
  width: 920px;
  height: auto;
  background: #ffffff;
  border-radius: 24px 0px 0px 24px;
  padding: 24px;
  box-sizing: border-box;
  display: flex;
}

.frame__dimmer {
  position: absolute;
  inset: 0;
  border: 0;
  background: rgba(10, 9, 14, 0.28);
  backdrop-filter: blur(2px);
  z-index: 10;
  pointer-events: auto;
  cursor: pointer;
  padding: 0;
}
</style>

