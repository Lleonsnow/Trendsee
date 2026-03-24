<script setup lang="ts">
import { nextTick, onBeforeUnmount, ref } from 'vue'
import type { Component } from 'vue'
import {
  BarChart3,
  Clapperboard,
  Eye,
  ExternalLink,
  Flame,
  Heart,
  MessageCircle,
  Play,
  Repeat2,
} from 'lucide-vue-next'

type Props = {
  videoSrc?: string
  dimmed?: boolean
  posterSrc?: string
  variant?: 'full' | 'thumb'
}

const props = defineProps<Props>()

type Stat = {
  label: string
  count: string
  variant: 'views' | 'likes' | 'comments' | 'reposts' | 'er'
  icon: Component
  iconColor: string
  iconBg: string
}

const stats: Stat[] = [
  {
    label: 'Просмотры',
    count: '12,3 млн',
    variant: 'views',
    icon: Eye,
    iconColor: '#2B31B3',
    iconBg: 'rgba(43, 49, 179, 0.12)',
  },
  {
    label: 'Лайки',
    count: '1,2 млн',
    variant: 'likes',
    icon: Heart,
    iconColor: '#D72E62',
    iconBg: 'rgba(215, 46, 98, 0.12)',
  },
  {
    label: 'Комментарии',
    count: '1,2 млн',
    variant: 'comments',
    icon: MessageCircle,
    iconColor: '#247A55',
    iconBg: 'rgba(36, 122, 85, 0.12)',
  },
  {
    label: 'Репосты',
    count: '1,2 млн',
    variant: 'reposts',
    icon: Repeat2,
    iconColor: '#B05A15',
    iconBg: 'rgba(176, 90, 21, 0.12)',
  },
  {
    label: 'ER',
    count: '1,2 млн',
    variant: 'er',
    icon: BarChart3,
    iconColor: '#2B31B3',
    iconBg: 'rgba(43, 49, 179, 0.12)',
  },
]

const captionText =
  'Чтобы выиграть в этой игре, нужно быть настоящим психопатом. Он с детства тасовал карты...'

const isCaptionExpanded = ref(false)
const isPlaying = ref(false)
const videoEl = ref<HTMLVideoElement | null>(null)
const viewerVideoEl = ref<HTMLVideoElement | null>(null)
const isViewerOpen = ref(false)
const isViewerLoading = ref(false)
const viewerLikes = ref(85_000)
const isAnalyzing = ref(false)
const isLikePressed = ref(false)
let analyzeTimer: ReturnType<typeof setTimeout> | null = null
let likeTimer: ReturnType<typeof setTimeout> | null = null

function toggleCaption() {
  isCaptionExpanded.value = !isCaptionExpanded.value
}

async function startVideo() {
  isViewerOpen.value = true
  isViewerLoading.value = true
  await nextTick()
  if (!viewerVideoEl.value) return
  try {
    await viewerVideoEl.value.play()
    isPlaying.value = true
  } catch {
    isPlaying.value = false
    isViewerLoading.value = false
  }
}

function syncPlayingState() {
  if (!videoEl.value) return
  isPlaying.value = !videoEl.value.paused
}

function syncViewerPlayingState() {
  if (!viewerVideoEl.value) return
  isPlaying.value = !viewerVideoEl.value.paused
}

function onViewerCanPlay() {
  isViewerLoading.value = false
}

function closeViewer() {
  isViewerOpen.value = false
  isViewerLoading.value = false
  if (viewerVideoEl.value) {
    viewerVideoEl.value.pause()
    viewerVideoEl.value.currentTime = 0
  }
  isPlaying.value = false
}

function formatCompactLikes(value: number): string {
  if (value >= 1_000_000) return `${Math.round((value / 1_000_000) * 10) / 10}M`
  if (value >= 1_000) return `${Math.round(value / 1_000)}k`
  return String(value)
}

function handleViewerLike() {
  viewerLikes.value += 1_000
  isLikePressed.value = true
  if (likeTimer) clearTimeout(likeTimer)
  likeTimer = setTimeout(() => {
    isLikePressed.value = false
    likeTimer = null
  }, 260)
}

function runAnalyzeAnimation() {
  if (isAnalyzing.value) return
  isAnalyzing.value = true
  if (analyzeTimer) clearTimeout(analyzeTimer)
  analyzeTimer = setTimeout(() => {
    isAnalyzing.value = false
    analyzeTimer = null
  }, 2000)
}

onBeforeUnmount(() => {
  if (analyzeTimer) clearTimeout(analyzeTimer)
  if (likeTimer) clearTimeout(likeTimer)
})
</script>

<template>
  <section
    class="media-column"
    :class="[
      variant === 'thumb' ? 'media-column--thumb' : 'media-column--full',
      { 'media-column--dimmed': dimmed },
    ]"
  >
    <div class="media-video" :class="{ 'media-video--thumb': variant === 'thumb' }" aria-hidden="true">
      <video
        ref="videoEl"
        class="media-video__el"
        :poster="posterSrc ?? '/demo.jpg'"
        :src="props.videoSrc ?? '/test.mp4'"
        muted
        playsinline
        preload="metadata"
        @play="syncPlayingState"
        @pause="syncPlayingState"
        @ended="syncPlayingState"
      />
      <div v-if="variant !== 'thumb'" class="media-video__tags">
        <span class="media-video__tag">
          <Clapperboard :size="14" :stroke-width="2.2" />
          Reels
        </span>
        <span class="media-video__tag">
          <Flame :size="14" :stroke-width="2.2" />
          x10
        </span>
      </div>
      <div v-if="!isPlaying" class="media-video__overlay">
        <button type="button" class="media-video__play" aria-label="Запустить видео" @click.stop="startVideo">
          <Play :size="24" :stroke-width="2.4" color="#FFFFFF" />
        </button>
      </div>
      <div v-if="dimmed" class="media-video__dim" aria-hidden="true" />
    </div>

    <div v-if="variant !== 'thumb'" class="stats" aria-label="Статистика">
      <div class="media-meta">
        <div class="media-meta__date">12.12.2025</div>
        <button class="media-meta__link" type="button" aria-label="Открыть оригинал">
          <ExternalLink :size="15" :stroke-width="2.2" />
        </button>
      </div>

      <div class="media-author">
        <img class="media-author__avatar" src="/Avatar.png" alt="Аватар автора" />
        <div class="media-author__text">
          <div class="media-author__name">@blogerich</div>
          <div class="media-author__followers">384.5K</div>
        </div>
      </div>

      <div class="media-caption">
        <div class="media-caption__text" :class="{ 'media-caption__text--expanded': isCaptionExpanded }">
          {{ captionText }}
        </div>
        <button type="button" class="media-caption__more" @click="toggleCaption">
          {{ isCaptionExpanded ? 'Свернуть' : 'Ещё' }}
        </button>
      </div>

      <div v-for="s in stats" :key="s.variant" class="stat-row" :class="`stat-row--${s.variant}`">
        <div class="stat-labelWrap">
          <span class="stat-icon" :style="{ background: s.iconBg }" aria-hidden="true">
            <component :is="s.icon" :size="14" :stroke-width="2.2" :style="{ color: s.iconColor }" />
          </span>
          <span class="stat-label">{{ s.label }}</span>
        </div>
        <span class="stat-count">{{ s.count }}</span>
      </div>
    </div>

    <div v-if="isViewerOpen" class="viewer" role="dialog" aria-modal="true">
      <button type="button" class="viewer__backdrop" aria-label="Закрыть просмотр" @click="closeViewer" />
      <div class="viewer__phone">
        <div class="viewer__videoWrap">
          <div class="viewer__topLeft">
            <span class="viewer__chip">
              <Clapperboard :size="14" :stroke-width="2.2" />
              Reels
            </span>
            <span class="viewer__chip">
              <Flame :size="14" :stroke-width="2.2" />
              x10
            </span>
          </div>
          <div class="viewer__topRight">
            <button
              class="viewer__iconBtn viewer__iconBtn--like"
              :class="{ 'viewer__iconBtn--like-active': isLikePressed }"
              type="button"
              aria-label="Лайк"
              @click="handleViewerLike"
            >
              <Heart :size="18" :stroke-width="2.2" />
            </button>
            <button class="viewer__iconBtn" type="button" aria-label="Открыть">
              <ExternalLink :size="18" :stroke-width="2.2" />
            </button>
          </div>
          <video
            ref="viewerVideoEl"
            class="viewer__video"
            :src="props.videoSrc ?? '/test.mp4'"
            :poster="posterSrc ?? '/demo.jpg'"
            controls
            playsinline
            preload="metadata"
            @canplay="onViewerCanPlay"
            @play="syncViewerPlayingState"
            @pause="syncViewerPlayingState"
            @ended="syncViewerPlayingState"
          />
          <div class="viewer__metrics">
            <span class="viewer__metric">
              <Eye :size="16" :stroke-width="2.2" />
              105k
            </span>
            <span class="viewer__metric">
              <Heart :size="16" :stroke-width="2.2" />
              {{ formatCompactLikes(viewerLikes) }}
            </span>
            <span class="viewer__metric">
              <MessageCircle :size="16" :stroke-width="2.2" />
              15k
            </span>
            <span class="viewer__metric">
              <Repeat2 :size="16" :stroke-width="2.2" />
              485
            </span>
          </div>
          <div v-if="isViewerLoading" class="viewer__loading" aria-label="Загрузка видео">
            <span class="viewer__spinner" />
          </div>
        </div>

        <div class="viewer__panel">
          <div class="viewer__card">
            <div class="viewer__authorRow">
              <div class="viewer__authorMain">
                <img class="viewer__avatar" src="/Avatar.png" alt="Аватар автора" />
                <div class="viewer__authorText">
                  <div class="viewer__authorName">@blogerich</div>
                  <div class="viewer__authorFollowers">384.5K</div>
                </div>
              </div>
              <button class="viewer__iconGhost" type="button" aria-label="Инструменты">
                <Sparkles :size="18" :stroke-width="2.2" />
              </button>
            </div>

            <p class="viewer__desc">500 000 лайков на ютубе делаем, бля буду скидываю 😂😂</p>
            <div class="viewer__date">12.12.2025</div>

            <button class="viewer__cta" :class="{ 'viewer__cta--loading': isAnalyzing }" type="button" @click="runAnalyzeAnimation">
              <span class="viewer__ctaLabel" :class="{ 'viewer__ctaLabel--hidden': isAnalyzing }">Анализ</span>
              <span class="viewer__ctaLoading" :class="{ 'viewer__ctaLoading--visible': isAnalyzing }" aria-live="polite">
                <span class="viewer__ctaSpinner" />
                Анализируем...
              </span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.media-column {
  background: #ffffff;
  width: 216px;
  min-height: 0;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  gap: 16px;
  box-sizing: border-box;
}

.media-column--thumb {
  width: 136px;
  min-height: 136px;
  justify-content: flex-start;
}

.media-column--full {
  width: 216px;
  height: 100%;
}

.media-video {
  width: 216px;
  aspect-ratio: 216 / 340;
  height: auto;
  border-radius: 18px;
  overflow: hidden;
  position: relative;
  background: #000;
  box-shadow: 0 10px 24px rgba(16, 24, 40, 0.16);
  isolation: isolate;
}

.media-video__tags {
  position: absolute;
  left: 8px;
  top: 8px;
  z-index: 2;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.media-video__tag {
  height: 28px;
  padding: 0 10px;
  border-radius: 10px;
  background: rgba(16, 24, 40, 0.58);
  color: #ffffff;
  font-family: var(--heading);
  font-size: 14px;
  font-weight: 500;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.media-video--thumb {
  width: 136px;
  aspect-ratio: 136 / 220;
  height: auto;
  border-radius: 16px;
  box-shadow: 0 8px 18px rgba(16, 24, 40, 0.14);
}

.media-video__el {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.media-video__overlay {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(180deg, rgba(8, 10, 19, 0.05) 0%, rgba(8, 10, 19, 0.25) 100%);
}

.media-video__play {
  width: 58px;
  height: 58px;
  border-radius: 999px;
  background: rgba(13, 18, 36, 0.5);
  backdrop-filter: blur(4px);
  border: 1px solid rgba(255, 255, 255, 0.34);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: 0;
  cursor: pointer;
}

.media-video__dim {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.28);
}

.media-column--dimmed {
  filter: blur(2px) brightness(0.82);
  transition: filter 0.2s ease;
}

.stats {
  width: 216px;
  flex: 1;
  min-height: 0;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 0;
  gap: 10px;
  box-sizing: border-box;
}

.media-meta {
  width: 216px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.media-meta__date {
  font-family: var(--heading);
  font-weight: 500;
  font-size: 12px;
  line-height: 14px;
  color: #83939c;
}

.media-meta__link {
  width: 22px;
  height: 22px;
  border: 0;
  border-radius: 8px;
  background: transparent;
  color: #667a85;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.media-author {
  width: 216px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.media-author__avatar {
  width: 32px;
  height: 32px;
  border-radius: 999px;
  object-fit: cover;
  display: block;
  flex: none;
}

.media-author__text {
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.media-author__name {
  font-family: var(--heading);
  font-weight: 600;
  font-size: 14px;
  line-height: 18px;
  color: #2b31b3;
}

.media-author__followers {
  font-family: var(--heading);
  font-weight: 500;
  font-size: 12px;
  line-height: 14px;
  color: #4e616b;
}

.media-caption {
  width: 216px;
}

.media-caption__text {
  font-family: var(--sans);
  font-weight: 400;
  font-size: 12px;
  line-height: 16px;
  color: #2f3f49;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  overflow: hidden;
}

.media-caption__text--expanded {
  display: block;
  -webkit-line-clamp: unset;
  line-clamp: unset;
}

.media-caption__more {
  margin-top: 2px;
  border: 0;
  background: transparent;
  padding: 0;
  font-family: var(--heading);
  font-weight: 700;
  font-size: 12px;
  line-height: 16px;
  color: #171c1f;
}

.stat-row {
  width: 216px;
  min-height: 40px;
  padding: 8px 10px;
  gap: 10px;
  background: #f4f5f6;
  border-radius: 16px;
  border: 0;
  display: flex;
  flex-direction: row;
  align-items: center;
  box-sizing: border-box;
}

.stat-labelWrap {
  min-width: 0;
  height: 16px;
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 8px;
  flex-grow: 1;
  box-sizing: border-box;
}

.stat-icon {
  width: 20px;
  height: 20px;
  border-radius: 6px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.stat-label {
  font-family: var(--sans);
  font-weight: 500;
  font-size: 12px;
  line-height: 14px;
  letter-spacing: 0.4px;
  color: #344054;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.stat-count {
  min-width: 72px;
  height: 21px;
  display: flex;
  align-items: center;
  font-family: var(--sans);
  font-weight: 600;
  font-size: 14px;
  line-height: 21px;
  letter-spacing: 0.25px;
  color: #101828;
  justify-content: flex-end;
  white-space: nowrap;
}

.viewer {
  position: fixed;
  inset: 0;
  z-index: 120;
  display: grid;
  place-items: center;
}

.viewer__backdrop {
  position: absolute;
  inset: 0;
  border: 0;
  padding: 0;
  background: rgba(8, 10, 18, 0.62);
  backdrop-filter: blur(4px);
}

.viewer__phone {
  position: relative;
  width: min(402px, calc(100vw - 28px));
  aspect-ratio: 402 / 874;
  max-height: min(90svh, 874px);
  background: #e6e8ec;
  border-radius: 32px;
  overflow: hidden;
  box-shadow: 0 24px 60px rgba(0, 0, 0, 0.42);
  z-index: 1;
  display: flex;
  flex-direction: column;
}

.viewer__videoWrap {
  position: relative;
  flex: 1;
  min-height: 0;
  border-radius: 0 0 26px 26px;
  overflow: hidden;
  background: #ffffff;
  padding: 8px;
  box-sizing: border-box;
}

.viewer__video {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
  border-radius: 24px;
}

.viewer__topLeft {
  position: absolute;
  top: 20px;
  left: 20px;
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 6px;
}

.viewer__chip {
  height: 30px;
  padding: 0 10px;
  border-radius: 10px;
  background: rgba(16, 24, 40, 0.58);
  color: #ffffff;
  font-family: var(--heading);
  font-size: 14px;
  line-height: 20px;
  font-weight: 500;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.viewer__panel {
  margin-top: -8px;
  background: #e6e8ec;
  border-radius: 18px 18px 0 0;
  padding: 12px 10px 12px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.viewer__topRight {
  position: absolute;
  top: 20px;
  right: 20px;
  z-index: 2;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.viewer__iconBtn {
  width: 32px;
  height: 32px;
  border: 0;
  border-radius: 10px;
  background: rgba(16, 24, 40, 0.58);
  color: #fff;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition:
    transform 0.18s ease,
    background-color 0.18s ease,
    box-shadow 0.18s ease,
    color 0.18s ease;
}

.viewer__iconBtn:hover {
  transform: translateY(-1px);
  background: rgba(16, 24, 40, 0.72);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.22);
}

.viewer__iconBtn:active {
  transform: scale(0.96);
}

.viewer__iconBtn--like {
  position: relative;
}

.viewer__iconBtn--like-active {
  color: #ff5b8f;
  background: rgba(255, 91, 143, 0.18);
  box-shadow: 0 0 0 0 rgba(255, 91, 143, 0.45);
  animation: likePulse 0.26s ease;
}

.viewer__metrics {
  position: absolute;
  left: 8px;
  right: 8px;
  bottom: 14px;
  height: 56px;
  border-radius: 18px;
  background: rgba(12, 16, 31, 0.58);
  backdrop-filter: blur(6px);
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  align-items: center;
  padding: 0 8px;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.22);
  z-index: 2;
}

.viewer__metric {
  color: #fff;
  font-family: var(--heading);
  font-size: 14px;
  font-weight: 500;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

.viewer__card {
  border-radius: 16px;
  background: #fdfdff;
  border: 1px solid rgba(16, 24, 40, 0.08);
  padding: 10px;
  box-sizing: border-box;
}

.viewer__authorRow {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.viewer__authorMain {
  display: flex;
  align-items: center;
  gap: 8px;
}

.viewer__avatar {
  width: 32px;
  height: 32px;
  border-radius: 999px;
  object-fit: cover;
}

.viewer__authorText {
  display: flex;
  flex-direction: column;
  gap: 1px;
}

.viewer__authorName {
  color: #2b31b3;
  font-family: var(--heading);
  font-size: 16px;
  line-height: 20px;
  font-weight: 700;
}

.viewer__authorFollowers {
  color: #4e616b;
  font-family: var(--heading);
  font-size: 13px;
  line-height: 16px;
}

.viewer__iconGhost {
  width: 30px;
  height: 30px;
  border: 0;
  border-radius: 10px;
  background: transparent;
  color: #2b31b3;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.viewer__desc {
  margin: 8px 0 4px;
  color: #4e616b;
  font-family: var(--sans);
  font-size: 13px;
  line-height: 17px;
}

.viewer__date {
  color: #9aa5ae;
  font-family: var(--heading);
  font-size: 12px;
  line-height: 14px;
  margin-bottom: 8px;
}

.viewer__cta {
  width: 100%;
  height: 40px;
  border: 0;
  border-radius: 12px;
  background: #2b31b3;
  color: #fff;
  font-family: var(--heading);
  font-size: 18px;
  line-height: 24px;
  font-weight: 600;
  position: relative;
  overflow: hidden;
  transition: background-color 0.2s ease, opacity 0.2s ease;
  cursor: pointer;
}

.viewer__cta--loading {
  background: #262b9f;
}

.viewer__ctaLabel {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  opacity: 1;
  transition: opacity 0.2s ease;
}

.viewer__ctaLabel--hidden {
  opacity: 0;
}

.viewer__ctaLoading {
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

.viewer__ctaLoading--visible {
  opacity: 1;
}

.viewer__ctaSpinner {
  width: 16px;
  height: 16px;
  border-radius: 999px;
  border: 2px solid rgba(255, 255, 255, 0.35);
  border-top-color: #ffffff;
  animation: spin 0.75s linear infinite;
}

.viewer__loading {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(7, 10, 18, 0.42);
}

.viewer__spinner {
  width: 38px;
  height: 38px;
  border-radius: 999px;
  border: 3px solid rgba(255, 255, 255, 0.28);
  border-top-color: #ffffff;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@keyframes likePulse {
  0% {
    transform: scale(1);
    box-shadow: 0 0 0 0 rgba(255, 91, 143, 0.45);
  }
  50% {
    transform: scale(1.08);
    box-shadow: 0 0 0 10px rgba(255, 91, 143, 0);
  }
  100% {
    transform: scale(1);
    box-shadow: 0 0 0 0 rgba(255, 91, 143, 0);
  }
}
</style>

