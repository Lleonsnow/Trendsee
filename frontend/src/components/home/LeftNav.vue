<script setup lang="ts">
import type { Component } from 'vue'
import { useRouter } from 'vue-router'
import {
  ArrowLeftRight,
  Bot,
  ChevronDown,
  ChevronRight,
  Clapperboard,
  Eye,
  FilePenLine,
  Film,
  Flame,
  House,
  Images,
  LogOut,
  Radar,
  ScanSearch,
  Sparkles,
} from 'lucide-vue-next'

type NavItem = {
  id: string
  label: string
  active?: boolean
  badge?: string
  iconColor: string
  icon: Component
}

type NavSection = {
  id: string
  title: string
  items: NavItem[]
}

const router = useRouter()

const sections: NavSection[] = [
  {
    id: 'main',
    title: '',
    items: [
      { id: 'home', label: 'Главная', iconColor: '#E99B00', icon: House },
      { id: 'video', label: 'Видео', active: true, iconColor: '#2B31B3', icon: Clapperboard },
      { id: 'spy', label: 'Шпионаж', iconColor: '#5E5B7D', icon: Eye },
      { id: 'radar', label: 'Контент радар', badge: '712', iconColor: '#333CD3', icon: Radar },
    ],
  },
  {
    id: 'social',
    title: 'Работа с соцсетями',
    items: [
      { id: 'cross', label: 'Кросс-постинг', iconColor: '#914CFF', icon: ArrowLeftRight },
      { id: 'bots', label: 'Чат боты', iconColor: '#FF3DBA', icon: Bot },
    ],
  },
  {
    id: 'tools',
    title: 'Инструменты',
    items: [
      { id: 'ai', label: 'ИИ-сценарий', iconColor: '#009CCF', icon: Sparkles },
      { id: 'carousels', label: 'Карусели', iconColor: '#914CFF', icon: Images },
      { id: 'analysis-video', label: 'Анализ видео', iconColor: '#009CCF', icon: Film },
      { id: 'analysis-profile', label: 'Анализ профиля', iconColor: '#4E616B', icon: ScanSearch },
      { id: 'draft', label: 'Черновик', iconColor: '#83939C', icon: FilePenLine },
    ],
  },
]

const tokens = {
  title: 'ТОКЕНЫ',
  current: 1245,
  total: 4497,
}

const account = {
  name: 'Александра',
  phone: '+7 (999) 999-99-99',
}

const progressPercent = Math.round((tokens.current / tokens.total) * 1000) / 10

function onNavItemClick(item: NavItem) {
  if (item.id === 'home') {
    void router.push({ name: 'feed' })
    return
  }

  void router.push({
    name: 'stub',
    query: { title: item.label },
  })
}
</script>

<template>
  <aside class="nav">
    <div class="nav__logoWrap">
      <img class="nav__logo" src="/Logo_full.png" alt="trends ee" />
    </div>
    <div class="nav__heading">Поиск контента</div>

    <div class="nav__list">
      <template v-for="section in sections" :key="section.id">
        <div v-if="section.title" class="nav__sectionTitle">{{ section.title }}</div>
        <div class="nav__items">
          <button
            v-for="item in section.items"
            :key="item.id"
            type="button"
            class="nav__item"
            :class="{ 'nav__item--active': item.active }"
            @click="onNavItemClick(item)"
          >
            <span class="nav__icon" aria-hidden="true">
              <component :is="item.icon" :size="20" :stroke-width="2.2" :style="{ color: item.iconColor }" />
            </span>
            <span class="nav__label">{{ item.label }}</span>
            <span v-if="item.badge" class="nav__badge">{{ item.badge }}</span>
          </button>
        </div>
      </template>
    </div>

    <div class="nav__bottom">
      <div class="nav__tarif">
        <div class="nav__tokens">
          <div class="nav__tokensTop">
            <div class="nav__tokensLabel">
              <Flame :size="18" :stroke-width="2.25" color="#ED003D" />
              <div class="nav__tokensTitle">{{ tokens.title }}</div>
            </div>
            <div class="nav__tokensValue">
              {{ tokens.current.toLocaleString('ru-RU') }} / {{ tokens.total.toLocaleString('ru-RU') }}
            </div>
          </div>

          <div class="nav__progress" aria-hidden="true">
            <div class="nav__progressTrack" :style="{ width: `${progressPercent}%` }" />
          </div>

          <button class="nav__creative" type="button">
            <span class="nav__creativeText">Creative +</span>
            <ChevronRight :size="18" :stroke-width="2.25" color="#667A85" />
          </button>
        </div>
      </div>

      <button class="nav__account" type="button">
        <span class="nav__avatar" aria-hidden="true">A</span>
        <span class="nav__accountContent">
          <span class="nav__accountName">{{ account.name }}</span>
          <span class="nav__accountSub">{{ account.phone }}</span>
        </span>
        <span class="nav__logout" aria-label="Выйти">
          <LogOut :size="17" :stroke-width="2.25" color="#667A85" />
        </span>
      </button>

      <button class="nav__language" type="button">
        <span class="nav__flagRu" aria-hidden="true" />
        <span class="nav__languageText">RU</span>
        <ChevronDown :size="16" :stroke-width="2.25" color="#667A85" />
      </button>
    </div>
  </aside>
</template>

<style scoped>
.nav {
  width: 274px;
  height: fit-content;
  background: #f4f5f6;
  border-radius: 16px;
  padding: 12px 16px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  gap: 8px;
  overflow: visible;
}

.nav__heading {
  font-family: var(--heading);
  font-weight: 600;
  font-size: 14px;
  line-height: 21px;
  letter-spacing: 0.1px;
  color: #83939c;
}

.nav__logoWrap {
  width: 100%;
  height: 40px;
  display: flex;
  align-items: center;
}

.nav__logo {
  height: 28px;
  width: auto;
  display: block;
}

.nav__list {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 24px;
  overflow: visible;
}

.nav__sectionTitle {
  width: 100%;
  height: 21px;
  font-family: var(--heading);
  font-weight: 600;
  font-size: 14px;
  line-height: 21px;
  letter-spacing: 0.1px;
  color: #83939c;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.nav__items {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.nav__item {
  width: 100%;
  height: 40px;
  border-radius: 12px;
  border: 0;
  background: #f4f5f6;
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 8px;
  box-sizing: border-box;
  cursor: pointer;
}

.nav__item--active {
  background: #f4f5f6;
}

.nav__icon {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.nav__label {
  flex: 1;
  min-width: 0;
  font-family: var(--heading);
  font-weight: 600;
  font-size: 14px;
  line-height: 21px;
  letter-spacing: 0.5px;
  color: #4e616b;
  text-align: left;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.nav__item--active .nav__label {
  color: #2b31b3;
}

.nav__badge {
  width: 45px;
  height: 21px;
  border-radius: 1000px;
  background: rgba(43, 49, 179, 0.12);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--heading);
  font-weight: 600;
  font-size: 14px;
  line-height: 21px;
  color: #2b31b3;
}

.nav__bottom {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex: none;
}

.nav__tarif {
  width: 100%;
  height: 94px;
  background: #ffffff;
  border-radius: 12px;
  padding: 12px;
  box-sizing: border-box;
}

.nav__tokens {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.nav__tokensTop {
  width: 100%;
  height: 21px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 6px;
}

.nav__tokensLabel {
  display: flex;
  align-items: center;
  gap: 4px;
}

.nav__tokensTitle {
  font-family: var(--heading);
  font-style: italic;
  font-weight: 700;
  font-size: 14px;
  line-height: 21px;
  letter-spacing: 0.25px;
  color: #000000;
  white-space: nowrap;
}

.nav__tokensValue {
  font-family: var(--heading);
  font-weight: 400;
  font-size: 14px;
  line-height: 21px;
  color: #000000;
  letter-spacing: 0.25px;
  white-space: nowrap;
}

.nav__progress {
  width: 100%;
  height: 8px;
  background: #e6e8ea;
  border-radius: 200px;
  position: relative;
  overflow: hidden;
}

.nav__progressTrack {
  height: 100%;
  background: #2b31b3;
  border-radius: 100px;
}

.nav__creative {
  width: 100%;
  height: 21px;
  border: 0;
  background: transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 2px;
  padding: 0;
  cursor: default;
}

.nav__creativeText {
  font-family: var(--heading);
  font-weight: 500;
  font-size: 14px;
  line-height: 21px;
  letter-spacing: 0.25px;
  color: #83939c;
}

.nav__account {
  width: 100%;
  height: 48px;
  border: 0;
  background: #f4f5f6;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px;
  box-sizing: border-box;
  cursor: default;
}

.nav__avatar {
  width: 32px;
  height: 32px;
  border-radius: 128px;
  background: linear-gradient(180deg, #8b8f9e 0%, #6d7388 100%);
  color: #ffffff;
  font-family: var(--heading);
  font-size: 12px;
  font-weight: 700;
  line-height: 1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex: none;
}

.nav__accountContent {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0;
}

.nav__accountName {
  width: 100%;
  font-family: var(--heading);
  font-weight: 500;
  font-size: 14px;
  line-height: 21px;
  letter-spacing: 0.25px;
  color: #4e616b;
  text-align: left;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.nav__accountSub {
  width: 100%;
  font-family: var(--heading);
  font-weight: 400;
  font-size: 12px;
  line-height: 16px;
  letter-spacing: 0.4px;
  color: #83939c;
  text-align: left;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.nav__logout {
  width: 24px;
  height: 24px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex: none;
}

.nav__language {
  width: 97px;
  height: 32px;
  border: 0;
  background: transparent;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  cursor: default;
}

.nav__flagRu {
  width: 24px;
  height: 16px;
  border-radius: 2px;
  border: 1.14286px solid rgba(0, 0, 0, 0.1);
  box-sizing: border-box;
  background: linear-gradient(
    to bottom,
    #ffffff 0%,
    #ffffff 33.33%,
    #0034a9 33.33%,
    #0034a9 66.66%,
    #d7280f 66.66%,
    #d7280f 100%
  );
}

.nav__languageText {
  font-family: var(--heading);
  font-weight: 500;
  font-size: 12px;
  line-height: 14px;
  letter-spacing: 0.4px;
  color: #83939c;
}
</style>

