<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { Clock3, Copy, Music2, WandSparkles, X } from 'lucide-vue-next'
import EssenceBlock from './EssenceBlock.vue'
import TranscriptionBlock from './TranscriptionBlock.vue'
import MediaPanel from './MediaPanel.vue'
import type { Post } from '../../types/posts'
import { fetchUserPostsPage } from '../../services/postsApi'
import { formatRuDate } from '../../utils/date'

type Props = {
  selectedPost: Post | null
}

const props = defineProps<Props>()

const emit = defineEmits<{
  (e: 'select', post: Post): void
  (e: 'clear'): void
}>()

const posts = ref<Post[]>([])
const isLoading = ref(false)
const isPageLoading = ref(false)
const hasMore = ref(true)
const pageSize = 6

const videoTopicLabel = 'Тема видео'
const musicLabel = 'Tyga – Pop it off'
const languageLabel = 'Английский'
const languageFlag = '🇬🇧'

const postBadges = [
  { id: 'tutorial', label: 'Туториал', bg: '#D5D6F8', color: '#2B31B3' },
  { id: 'energetic', label: 'Энергичное видео', bg: '#E1F7D8', color: '#1E6D00' },
  { id: 'montage', label: 'Изи монтаж', bg: '#FFE9C7', color: '#A24C00' },
  { id: 'trendy', label: 'Трендовый звук', bg: '#FDE4EB', color: '#C5003B' },
  { id: 'lead', label: 'Лид магнит', bg: '#FFF0CB', color: '#9E3F00' },
  { id: 'beauty', label: 'Красота и здоровье', bg: '#D5D6F8', color: '#2B31B3' },
]

const structureSteps = [
  {
    id: 'hook',
    time: '0–3 сек',
    title: 'Шок-сравнение',
    description: 'Визуальный (Девушка с предметом) + Текст на экране:\n"Это спасет вашу зиму"',
    dot: 'dashed' as const,
  },
  {
    id: 'value',
    time: '3–15 сек',
    title: 'Сюжет',
    description: '[Герой] показывает проблему -> Резкая смена кадра -> Решение',
    dot: 'outline' as const,
  },
  {
    id: 'cta',
    time: '15–120 сек',
    title: 'Финал / CTA',
    description: 'Призыв: "Пиши слово \"ССЫЛКА\" в комменты"',
    dot: 'filled' as const,
  },
]

const hookPhrases = [
  {
    id: 'hook-1',
    title: 'Хук фраза 1',
    description: 'Это спасет вашу зиму',
  },
  {
    id: 'hook-2',
    title: 'Хук фраза 2',
    description: 'Ты точно делаешь это неправильно каждое утро',
  },
  {
    id: 'hook-3',
    title: 'Хук фраза 3',
    description: 'Один простой шаг, который экономит тебе десятки минут',
  },
]

const workingMethods = [
  {
    id: 'method-1',
    title: '2. Суть видео',
    lines: [
      'Приём: “кому подходит / кому нет” двумя блоками.',
      'Почему сработало: это формат “диагноз -> лечение -> решение”. Люди сохраняют не эмоции, а инструкцию. И это “обзор”, а не философия',
    ],
  },
  {
    id: 'method-2',
    title: '3. Монтаж',
    lines: [
      'Приём: смена планов каждые 1–2 секунды: лицо -> продукт крупно -> рука (демо) -> снова лицо.',
      'Почему сработало: вертикалки смотрят на автопилоте. Частая смена планов держит внимание даже без звука',
      'Приём: все доказательства — через B-roll вставки на 0.3–0.8 сек (катышки, блеск, этикетка, нанесение).',
      'Почему сработало: речь в кадре быстро утомляет. B-roll делает ощущение “я реально тестировал”.',
    ],
  },
  {
    id: 'method-3',
    title: '4. Реплики',
    lines: [
      'Приём: “триггер доверия” одной фразой: “Я не продаю этот SPF, мне пох, скажу как есть”.',
      'Почему сработало: снимает защиту “мне впаривают”.',
      'Приём: “вилка выбора” в середине: “Если кожа жирная — делай так. Если сухая — так.”',
      'Почему сработало: персонализация без долгого объяснения = удержание.',
    ],
  },
]

const marketingFunnel = [
  {
    id: 'cta',
    title: 'CTA голос/визуал',
    text: 'Почему сработало: зритель узнаёт свой баг мгновенно. Это не “мнение”, а физический факт в кадре, мозг цепляется.',
  },
  {
    id: 'trigger',
    title: 'Триггер',
    text: 'Почему сработало: зритель узнаёт свой баг мгновенно. Это не “мнение”, а физический факт в кадре, мозг цепляется.',
  },
  {
    id: 'destination',
    title: 'Куда ведет',
    text: 'Почему сработало: зритель узнаёт свой баг мгновенно. Это не “мнение”, а физический факт в кадре, мозг цепляется.',
  },
  {
    id: 'lead',
    title: 'Лид-магнит',
    text: 'Почему сработало: зритель узнаёт свой баг мгновенно. Это не “мнение”, а физический факт в кадре, мозг цепляется.',
  },
]

const curatedPostTitles = [
  'Рассуждения на тему правильности и неправильности',
  'Разбор типичных ошибок в ежедневном уходе',
  'Почему одни советы работают, а другие нет',
  'Короткий разбор: как принимать решения в бьюти-рутине',
  'Пошаговая логика: от проблемы к решению',
  'Практичный разбор без лишней теории',
]


onMounted(async () => {
  if (posts.value.length > 0) return
  await loadNextPage(true)
})

function posterSrcByIndex(index: number): string {
  if (index < 0) return '/demo.jpg'
  // Демо: ожидаем файлы в public/blogers/bloger_1.jpg ... bloger_4.jpg
  if (index > 3) return '/demo.jpg'
  return `/blogers/bloger_${index + 1}.jpg`
}

const selectedIndex = computed(() => {
  if (visiblePosts.value.length === 0 || !props.selectedPost) return -1
  return visiblePosts.value.findIndex((p) => p.id === props.selectedPost!.id)
})

const selectedPosterSrc = computed(() => {
  if (!props.selectedPost) return '/demo.jpg'
  if (selectedIndex.value < 0) return '/demo.jpg'
  return posterSrcByIndex(selectedIndex.value)
})

const visiblePosts = computed(() => {
  if (posts.value.length <= 2) return posts.value
  return posts.value.slice(0, -2)
})

const canLoadMore = computed(() => hasMore.value && !isLoading.value && !isPageLoading.value)

function emitSelect(post: Post) {
  emit('select', post)
}

function displayPostTitle(post: Post, index: number): string {
  const fallback = curatedPostTitles[index % curatedPostTitles.length]
  const raw = post.title?.trim() ?? ''
  if (!raw) return fallback
  return /^(Post|Пост)\s*#\d+$/i.test(raw) ? fallback : raw
}

function buildSemanticPreviewByTitle(title: string): string {
  const normalizedTitle = title.toLowerCase()

  if (normalizedTitle.includes('ошиб')) {
    return 'Короткий разбор частых ошибок и понятные шаги, как исправить их без лишней теории.'
  }

  if (normalizedTitle.includes('совет') || normalizedTitle.includes('работают')) {
    return 'Показываем, какие советы действительно дают результат, а какие создают только ложное ожидание.'
  }

  if (normalizedTitle.includes('решени') || normalizedTitle.includes('логик')) {
    return 'Последовательный путь от симптома к решению: на что смотреть в первую очередь и что делать дальше.'
  }

  if (normalizedTitle.includes('разбор')) {
    return 'Практичный разбор с акцентом на действия: что внедрить сразу, чтобы увидеть заметный эффект.'
  }

  return 'Содержательное превью публикации с краткой сутью, ключевой идеей и ожидаемым практическим результатом.'
}

function buildPostPreview(text: string, title: string): string {
  const normalized = text.replace(/\s+/g, ' ').trim()
  const isDemoText =
    /демо-текст/i.test(normalized) ||
    /позже вы подставите реальные данные/i.test(normalized) ||
    /^это демо/i.test(normalized)

  if (!normalized || isDemoText) return buildSemanticPreviewByTitle(title)
  return normalized.length > 96 ? `${normalized.slice(0, 96)}...` : normalized
}

async function loadNextPage(isInitial = false): Promise<void> {
  if (!isInitial && !canLoadMore.value) return

  if (isInitial) isLoading.value = true
  else isPageLoading.value = true

  try {
    const page = await fetchUserPostsPage({ offset: posts.value.length, limit: pageSize })
    posts.value = posts.value.concat(page.items)
    hasMore.value = page.has_more
  } finally {
    if (isInitial) isLoading.value = false
    else isPageLoading.value = false
  }
}

function onFeedScroll(event: Event): void {
  if (!canLoadMore.value) return
  const target = event.target as HTMLElement | null
  if (!target) return

  const remaining = target.scrollHeight - target.scrollTop - target.clientHeight
  if (remaining <= 500) {
    void loadNextPage(false)
  }
}
</script>

<template>
  <aside class="sidebar">
    <div
      class="sidebar__feed"
      :class="{ 'sidebar__feed--dimmed': props.selectedPost != null }"
      @scroll.passive="onFeedScroll"
    >
      <h2 class="sidebar__listTitle">Блогеры</h2>

      <div v-if="isLoading" class="sidebar__loading" role="status">Загрузка...</div>

      <button
        v-for="(p, idx) in visiblePosts"
        :key="p.id"
        type="button"
        class="blogger"
        :disabled="props.selectedPost != null"
        @click="emitSelect(p)"
      >
        <MediaPanel variant="thumb" :posterSrc="posterSrcByIndex(idx)" />
        <div class="blogger__body">
          <div class="blogger__name">{{ displayPostTitle(p, idx) }}</div>
          <div class="blogger__preview">{{ buildPostPreview(p.text, displayPostTitle(p, idx)) }}</div>
          <div class="blogger__meta">{{ formatRuDate(p.created_at) }}</div>
        </div>
      </button>

      <div v-if="isPageLoading" class="sidebar__loading sidebar__loading--more" role="status">
        Загружаем еще публикации...
      </div>
    </div>

    <Transition name="overlay-fade">
      <div v-if="props.selectedPost" class="sidebar__overlay">
        <div class="overlay__post">
          <MediaPanel variant="full" :posterSrc="selectedPosterSrc" />

          <div class="overlay__content">
            <div class="sidebar__topic">{{ videoTopicLabel }}</div>

          <div class="sidebar__detailsHeader">
            <h2 class="sidebar__detailsTitle">
              {{ displayPostTitle(props.selectedPost, selectedIndex >= 0 ? selectedIndex : 0) }}
            </h2>
            <button type="button" class="sidebar__close" aria-label="Закрыть" @click="emit('clear')">
              <X :size="18" :stroke-width="2.3" />
            </button>
          </div>

          <div class="sidebar__contextRow">
            <span class="sidebar__contextChip">
              <Music2 :size="14" :stroke-width="2.2" color="#F3B500" />
              {{ musicLabel }}
            </span>
            <span class="sidebar__langLabel">Язык:</span>
            <span class="sidebar__contextChip">
              <span class="sidebar__flagInline" aria-hidden="true">{{ languageFlag }}</span>
              {{ languageLabel }}
            </span>
          </div>

          <div class="sidebar__badges" aria-label="Инсайты поста">
            <span
              v-for="badge in postBadges"
              :key="badge.id"
              class="sidebar__badge"
              :style="{ background: badge.bg, color: badge.color }"
            >
              {{ badge.label }}
            </span>
          </div>

            <div class="sidebar__detailsData">
              <div class="sidebar__detailsDataRow">
                <span class="sidebar__detailsLabel">User ID:</span>
                <span class="sidebar__detailsValue">{{ props.selectedPost.user_id }}</span>
              </div>
              <div class="sidebar__detailsDataRow">
                <span class="sidebar__detailsLabel">Created at:</span>
                <span class="sidebar__detailsValue">{{ formatRuDate(props.selectedPost.created_at) }}</span>
              </div>
              <div class="sidebar__detailsDataRow">
                <span class="sidebar__detailsLabel">Updated at:</span>
                <span class="sidebar__detailsValue">{{ formatRuDate(props.selectedPost.updated_at) }}</span>
              </div>
              <div class="sidebar__detailsDataRow sidebar__detailsDataRow--full">
                <span class="sidebar__detailsLabel">Text:</span>
                <p class="sidebar__detailsText">{{ props.selectedPost.text }}</p>
              </div>
            </div>

            <TranscriptionBlock />
            <EssenceBlock />

            <section class="structure">
            <div class="structure__head">
              <h3 class="structure__title">Структура</h3>
            </div>

            <div class="structure__steps">
              <article v-for="step in structureSteps" :key="step.id" class="structure__step">
                <div class="structure__timeCol">
                  <div class="structure__timeLabel">
                    <Clock3 :size="14" :stroke-width="2.1" color="#A0ADB4" />
                    <span class="structure__time">{{ step.time }}</span>
                  </div>
                  <span class="structure__dot" :class="`structure__dot--${step.dot}`" aria-hidden="true" />
                  <div class="structure__line" aria-hidden="true" />
                </div>

                <div class="structure__desc">
                  <h4 class="structure__stepTitle">{{ step.title }}</h4>
                  <p class="structure__stepText">{{ step.description }}</p>
                </div>
              </article>
            </div>
            </section>

            <section class="hooks">
            <div class="hooks__card">
              <article v-for="hook in hookPhrases" :key="hook.id" class="hooks__item">
                <div class="hooks__itemHead">
                  <h3 class="hooks__title">{{ hook.title }}</h3>
                  <button class="hooks__iconBtn" type="button" aria-label="Действия для хук фразы">
                    <WandSparkles :size="16" :stroke-width="2.2" />
                  </button>
                </div>
                <p class="hooks__description">{{ hook.description }}</p>
              </article>
            </div>
            </section>

            <section class="insights">
            <div class="insights__head">
              <h3 class="insights__title">Рабочие приемы</h3>
              <button class="insights__iconBtn" type="button" aria-label="Действия по рабочим приемам">
                <Copy :size="16" :stroke-width="2.2" />
              </button>
            </div>

            <div class="insights__card">
              <article v-for="item in workingMethods" :key="item.id" class="insights__item">
                <h4 class="insights__itemTitle">{{ item.title }}</h4>
                <p v-for="(line, idx) in item.lines" :key="`${item.id}-${idx}`" class="insights__itemText">
                  {{ line }}
                </p>
              </article>
            </div>
            </section>

            <section class="marketing">
            <div class="marketing__head">
              <h3 class="marketing__title">Воронка / Маркетинг</h3>
              <button class="marketing__iconBtn" type="button" aria-label="Действия по воронке">
                <Copy :size="16" :stroke-width="2.2" />
              </button>
            </div>

            <div class="marketing__card">
              <article v-for="item in marketingFunnel" :key="item.id" class="marketing__item">
                <h4 class="marketing__itemTitle">{{ item.title }}</h4>
                <p class="marketing__itemText">{{ item.text }}</p>
              </article>
            </div>
            </section>

          </div>
        </div>
      </div>
    </Transition>
  </aside>
</template>

<style scoped>
.sidebar {
  position: relative;
  width: 100%;
  height: 100%;
  background: #ffffff;
  box-sizing: border-box;
  z-index: 20;
  border-radius: 20px;
  overflow: hidden;
}

.sidebar__feed {
  height: 100%;
  min-height: 0;
  overflow-y: auto;
  padding: 24px 18px 20px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  gap: 14px;
  transition: filter 0.2s ease, opacity 0.2s ease;
  border-radius: inherit;
  scrollbar-width: thin;
  scrollbar-color: rgba(43, 49, 179, 0.38) rgba(15, 23, 42, 0.06);
}

.sidebar__feed::-webkit-scrollbar {
  width: 8px;
}

.sidebar__feed::-webkit-scrollbar-track {
  background: rgba(15, 23, 42, 0.06);
  border-radius: 999px;
}

.sidebar__feed::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, rgba(43, 49, 179, 0.52) 0%, rgba(43, 49, 179, 0.34) 100%);
  border-radius: 999px;
  border: 1px solid rgba(255, 255, 255, 0.8);
}

.sidebar__feed::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(180deg, rgba(43, 49, 179, 0.68) 0%, rgba(43, 49, 179, 0.48) 100%);
}

.sidebar__feed--dimmed {
  pointer-events: none;
}

.sidebar__listTitle {
  margin: 0 0 8px;
  font-family: var(--heading);
  font-weight: 700;
  font-size: 17px;
  line-height: 24px;
  color: #111827;
}

.sidebar__loading {
  padding: 8px 0;
  color: var(--text, #6b6375);
}

.sidebar__loading--more {
  padding: 2px 4px 12px;
  font-size: 13px;
}

.blogger {
  width: 100%;
  display: flex;
  align-items: stretch;
  gap: 16px;
  border: 1px solid rgba(16, 24, 40, 0.08);
  border-radius: 20px;
  padding: 12px;
  background: #ffffff;
  cursor: pointer;
  text-align: left;
  transition: box-shadow 0.18s ease, border-color 0.18s ease, transform 0.18s ease;
}

.blogger:hover:not(:disabled) {
  border-color: rgba(43, 49, 179, 0.24);
  box-shadow: 0 14px 28px rgba(16, 24, 40, 0.12);
  transform: translateY(-2px);
}

.blogger:disabled {
  cursor: default;
}

.blogger__body {
  flex: 1;
  min-width: 0;
  padding: 10px 12px;
  display: flex;
  flex-direction: column;
  gap: 9px;
  justify-content: flex-start;
  border-radius: 14px;
  border: 1px solid rgba(16, 24, 40, 0.06);
  background: linear-gradient(180deg, #ffffff 0%, #f9fbff 100%);
}

.blogger__name {
  font-family: var(--heading);
  font-weight: 700;
  font-size: 16px;
  line-height: 22px;
  letter-spacing: 0.1px;
  color: #1f2a44;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.blogger__meta {
  font-family: var(--sans);
  font-weight: 600;
  font-size: 12px;
  line-height: 16px;
  color: #556176;
  white-space: nowrap;
  margin-top: auto;
  align-self: flex-start;
  padding: 4px 10px;
  border-radius: 999px;
  background: rgba(43, 49, 179, 0.08);
}

.blogger__preview {
  font-family: var(--sans);
  font-weight: 400;
  font-size: 13px;
  line-height: 19px;
  color: #5b667a;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.sidebar__overlay {
  position: absolute;
  inset: 0;
  background: #ffffff;
  overflow-y: auto;
  overflow-x: hidden;
  z-index: 30;
  border-radius: inherit;
  scrollbar-width: thin;
  scrollbar-color: rgba(43, 49, 179, 0.38) rgba(15, 23, 42, 0.06);
}

.sidebar__overlay::-webkit-scrollbar {
  width: 8px;
}

.sidebar__overlay::-webkit-scrollbar-track {
  background: rgba(15, 23, 42, 0.06);
  border-radius: 999px;
}

.sidebar__overlay::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, rgba(43, 49, 179, 0.52) 0%, rgba(43, 49, 179, 0.34) 100%);
  border-radius: 999px;
  border: 1px solid rgba(255, 255, 255, 0.8);
}

.sidebar__overlay::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(180deg, rgba(43, 49, 179, 0.68) 0%, rgba(43, 49, 179, 0.48) 100%);
}

.overlay__post {
  width: 100%;
  min-height: 100%;
  display: flex;
  gap: 24px;
  align-items: flex-start;
  padding: 24px;
  box-sizing: border-box;
}

.overlay__content {
  flex: 1;
  width: 100%;
  max-width: 624px;
  min-width: 0;
  padding-top: 2px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.sidebar__topic {
  font-family: var(--heading);
  font-weight: 500;
  font-size: 14px;
  line-height: 21px;
  letter-spacing: 0.25px;
  color: #4e616b;
}

.sidebar__detailsHeader {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  padding-bottom: 2px;
}

.sidebar__detailsTitle {
  margin: 0;
  font-family: var(--heading);
  font-weight: 700;
  font-size: clamp(24px, 2.4vw, 30px);
  line-height: 1.2;
  color: #08060d;
  flex: 1;
}

.sidebar__close {
  width: 36px;
  height: 36px;
  border-radius: 12px;
  border: 1px solid rgba(16, 24, 40, 0.14);
  background: #ffffff;
  cursor: pointer;
  color: #4b5563;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: border-color 0.18s ease, color 0.18s ease, box-shadow 0.18s ease;
}

.sidebar__close:hover {
  color: #1f2937;
  border-color: rgba(43, 49, 179, 0.36);
  box-shadow: 0 6px 14px rgba(16, 24, 40, 0.08);
}

.sidebar__contextRow {
  display: flex;
  align-items: center;
  gap: 8px;
}

.sidebar__contextChip {
  height: 32px;
  border-radius: 12px;
  background: #f4f5f6;
  color: #4e616b;
  font-family: var(--heading);
  font-weight: 500;
  font-size: 14px;
  line-height: 20px;
  letter-spacing: 0.25px;
  padding: 4px 10px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.sidebar__langLabel {
  font-family: var(--heading);
  font-weight: 500;
  font-size: 14px;
  line-height: 20px;
  letter-spacing: 0.25px;
  color: #4e616b;
}

.sidebar__flagInline {
  font-size: 14px;
  line-height: 1;
}

.sidebar__badges {
  width: 100%;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.sidebar__badge {
  min-height: 29px;
  border-radius: 1000px;
  padding: 4px 12px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-family: var(--heading);
  font-weight: 500;
  font-size: 14px;
  line-height: 21px;
  letter-spacing: 0.25px;
  white-space: nowrap;
}

.sidebar__detailsData {
  width: 100%;
  border: 1px solid rgba(16, 24, 40, 0.08);
  background: #ffffff;
  border-radius: 14px;
  padding: 12px 14px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  box-sizing: border-box;
}

.sidebar__detailsDataRow {
  display: flex;
  align-items: baseline;
  gap: 8px;
}

.sidebar__detailsDataRow--full {
  flex-direction: column;
  align-items: flex-start;
}

.sidebar__detailsLabel {
  font-family: var(--heading);
  font-size: 12px;
  line-height: 16px;
  font-weight: 600;
  color: #5b6471;
}

.sidebar__detailsValue {
  font-family: var(--sans);
  font-size: 13px;
  line-height: 18px;
  color: #111827;
}

.sidebar__detailsText {
  margin: 0;
  font-family: var(--sans);
  font-size: 14px;
  line-height: 21px;
  color: #334155;
  white-space: pre-wrap;
}

.overlay-fade-enter-active,
.overlay-fade-leave-active {
  transition: opacity 0.24s ease, transform 0.24s ease;
}

.overlay-fade-enter-from,
.overlay-fade-leave-to {
  opacity: 0;
  transform: translateY(8px);
}

.structure {
  width: 100%;
  max-width: 624px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.structure__head {
  width: 100%;
  height: 32px;
  display: flex;
  align-items: center;
  padding: 4px 0;
  box-sizing: border-box;
}

.structure__title {
  margin: 0;
  font-family: var(--heading);
  font-weight: 600;
  font-size: 16px;
  line-height: 24px;
  letter-spacing: 0.15px;
  color: #000000;
}

.structure__steps {
  width: 100%;
  display: flex;
  flex-direction: column;
  background: #f4f5f6;
  border-radius: 12px;
  padding: 16px;
  box-sizing: border-box;
}

.structure__step {
  width: 100%;
  min-height: 87px;
  display: flex;
  align-items: flex-start;
  gap: 8px;
}

.structure__timeCol {
  width: 128px;
  min-height: 87px;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  gap: 0;
}

.structure__timeLabel {
  width: 96px;
  height: 36px;
  display: flex;
  justify-content: flex-start;
  align-items: center;
  gap: 4px;
  padding: 10px 0 6px;
  box-sizing: border-box;
}

.structure__dot {
  width: 16px;
  height: 16px;
  border-radius: 999px;
  margin-left: 80px;
  box-sizing: border-box;
}

.structure__dot--dashed {
  border: 2px dashed #2b31b3;
  background: #ffffff;
}

.structure__dot--outline {
  border: 2px solid #2b31b3;
  background: #ffffff;
}

.structure__dot--filled {
  border: 2px solid #2b31b3;
  background: #2b31b3;
}

.structure__time {
  font-family: var(--heading);
  font-weight: 500;
  font-size: 12px;
  line-height: 14px;
  letter-spacing: 0.4px;
  color: #4e616b;
}

.structure__line {
  width: 1px;
  background: #aeb1f2;
  margin: 6px 0 0 87px;
  flex: 1;
}

.structure__step:last-child .structure__line {
  opacity: 0;
}

.structure__desc {
  width: min(400px, 100%);
  min-height: 87px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 8px 0 12px;
  box-sizing: border-box;
}

.structure__stepTitle {
  margin: 0;
  font-family: var(--heading);
  font-weight: 600;
  font-size: 14px;
  line-height: 21px;
  letter-spacing: 0.1px;
  color: #000000;
}

.structure__stepText {
  margin: 0;
  font-family: var(--sans);
  font-weight: 400;
  font-size: 14px;
  line-height: 21px;
  letter-spacing: 0.25px;
  color: #4e616b;
  white-space: pre-wrap;
}

.hooks {
  width: 100%;
  max-width: 624px;
}

.hooks__card {
  width: 100%;
  background: #f4f5f6;
  border-radius: 12px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 24px;
  box-sizing: border-box;
}

.hooks__item {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.hooks__itemHead {
  width: 100%;
  height: 32px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.hooks__title {
  margin: 0;
  flex: 1;
  min-width: 0;
  font-family: var(--heading);
  font-weight: 600;
  font-size: 16px;
  line-height: 24px;
  letter-spacing: 0.15px;
  color: #000000;
}

.hooks__iconBtn {
  width: 32px;
  height: 32px;
  border: 0;
  border-radius: 12px;
  background: #f4f5f6;
  color: #3a4951;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.hooks__description {
  margin: 0;
  font-family: var(--sans);
  font-weight: 400;
  font-size: 14px;
  line-height: 21px;
  letter-spacing: 0.25px;
  color: #4e616b;
}

.insights {
  width: 100%;
  max-width: 624px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.insights__head {
  width: 100%;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 10px;
}

.insights__title {
  margin: 0;
  width: auto;
  flex: 1;
  min-width: 0;
  font-family: var(--heading);
  font-weight: 600;
  font-size: 16px;
  line-height: 24px;
  letter-spacing: 0.15px;
  color: #000000;
}

.insights__iconBtn {
  width: 32px;
  height: 32px;
  border: 0;
  border-radius: 12px;
  background: #f4f5f6;
  color: #3a4951;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 8px;
  box-sizing: border-box;
}

.insights__card {
  width: 100%;
  min-height: 263px;
  background: #f4f5f6;
  border-radius: 12px;
  padding: 16px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.insights__item {
  width: 100%;
  height: auto;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.insights__itemTitle {
  margin: 0;
  width: 100%;
  font-family: var(--heading);
  font-weight: 600;
  font-size: 16px;
  line-height: 24px;
  letter-spacing: 0.15px;
  color: #000000;
}

.insights__itemText {
  margin: 0;
  width: 100%;
  min-height: 21px;
  font-family: var(--sans);
  font-weight: 400;
  font-size: 14px;
  line-height: 21px;
  letter-spacing: 0.25px;
  color: #4e616b;
}

.marketing {
  width: 100%;
  max-width: 624px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.marketing__head {
  width: 100%;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 10px;
}

.marketing__title {
  margin: 0;
  width: auto;
  flex: 1;
  min-width: 0;
  font-family: var(--heading);
  font-weight: 600;
  font-size: 16px;
  line-height: 24px;
  letter-spacing: 0.15px;
  color: #000000;
}

.marketing__iconBtn {
  width: 32px;
  height: 32px;
  border: 0;
  border-radius: 12px;
  background: #f4f5f6;
  color: #3a4951;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 8px;
  box-sizing: border-box;
}

.marketing__card {
  width: 100%;
  background: #f4f5f6;
  border-radius: 12px;
  padding: 16px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.marketing__item {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.marketing__itemTitle {
  margin: 0;
  width: 100%;
  font-family: var(--heading);
  font-weight: 600;
  font-size: 16px;
  line-height: 24px;
  letter-spacing: 0.15px;
  color: #000000;
}

.marketing__itemText {
  margin: 0;
  width: 100%;
  font-family: var(--sans);
  font-weight: 400;
  font-size: 14px;
  line-height: 21px;
  letter-spacing: 0.25px;
  color: #4e616b;
}

@media (max-width: 1180px) {
  .sidebar__feed {
    padding: 20px 14px 18px;
    gap: 12px;
  }

  .blogger {
    border-radius: 16px;
    padding: 10px;
    gap: 12px;
  }

  .blogger__body {
    gap: 8px;
  }

  .overlay__post {
    gap: 16px;
    padding-top: 20px;
  }
}
</style>

