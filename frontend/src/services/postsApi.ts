import type { Post, PostsPage } from '../types/posts'
import { API_ENDPOINTS } from './endpoints'
import { getJwtToken } from './storage'

function joinUrl(base: string, path: string): string {
  const trimmedBase = base.endsWith('/') ? base.slice(0, -1) : base
  const trimmedPath = path.startsWith('/') ? path : `/${path}`
  return `${trimmedBase}${trimmedPath}`
}

function makeMockPost(index: number): Post {
  const created = new Date(Date.now() - index * 36_00000) // roughly hourly steps
  const updated = new Date(created.getTime() + 4_200_000)

  const title = `Пост #${index + 1}`
  const text =
    `Это демо-текст для карточки поста №${index + 1}. ` +
    `Позже вы подставите реальные данные из бэкенда и этот мок отключим.`

  return {
    id: String(index + 1),
    user_id: '1',
    title,
    text,
    created_at: created.toISOString(),
    updated_at: updated.toISOString(),
  }
}

async function fetchUserPostsFromApi(params: {
  offset: number
  limit: number
}): Promise<PostsPage> {
  const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? ''
  if (!apiBaseUrl) {
    throw new Error('VITE_API_BASE_URL не задан')
  }

  const url = new URL(joinUrl(apiBaseUrl, API_ENDPOINTS.userPosts))
  url.searchParams.set('offset', String(params.offset))
  url.searchParams.set('limit', String(params.limit))

  const token = getJwtToken()
  const headers: HeadersInit = {
    Accept: 'application/json',
  }
  if (token) headers.Authorization = `Bearer ${token}`

  const res = await fetch(url, {
    method: 'GET',
    headers,
  })

  if (!res.ok) {
    const bodyText = await res.text().catch(() => '')
    throw new Error(
      `Ошибка загрузки постов: ${res.status} ${res.statusText}${bodyText ? `: ${bodyText}` : ''}`,
    )
  }

  const data: unknown = await res.json()

  // Ожидаем одно из: { items, has_more } или { posts, hasMore }.
  const obj = (data && typeof data === 'object' ? data : {}) as Record<string, unknown>
  const rawItems = (obj.items ?? obj.posts) as unknown

  const items = Array.isArray(rawItems)
    ? (rawItems.filter(Boolean) as Post[])
    : ([] as Post[])

  const hasMoreValue =
    (obj.has_more as unknown) ??
    (obj.hasMore as unknown) ??
    (obj.hasMoreValue as unknown)

  const has_more = typeof hasMoreValue === 'boolean' ? hasMoreValue : items.length === params.limit

  return { items, has_more }
}

async function fetchUserPostsMock(params: {
  offset: number
  limit: number
}): Promise<PostsPage> {
  // Небольшая задержка, чтобы увидеть индикатор загрузки.
  await new Promise((r) => setTimeout(r, 350))

  const total = 47
  const start = params.offset
  const endExclusive = Math.min(total, start + params.limit)
  const items: Post[] = []

  for (let i = start; i < endExclusive; i++) {
    items.push(makeMockPost(i))
  }

  return {
    items,
    has_more: endExclusive < total,
  }
}

export async function fetchUserPostsPage(params: {
  offset: number
  limit: number
}): Promise<PostsPage> {
  const useMock =
    import.meta.env.VITE_USE_MOCK === 'true' || !(import.meta.env.VITE_API_BASE_URL ?? '')

  if (useMock) {
    return fetchUserPostsMock(params)
  }

  return fetchUserPostsFromApi(params)
}

