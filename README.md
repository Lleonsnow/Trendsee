# Trendsee

Платформа для работы с контентом: backend на FastAPI и frontend на Vue 3.

## Структура проекта

- `backend` — API, JWT-авторизация, работа с Postgres и Redis.
- `frontend` — клиентское приложение на Vue 3 + Vite + TypeScript.
- `docker-compose.yml` — инфраструктура для локального запуска backend-сервисов.

## Требования

- Docker + Docker Compose
- Node.js 20+
- npm 10+

## Быстрый старт

### 1) Запуск backend

```bash
docker compose up --build
```

Backend API: `http://localhost:8000`

### 2) Запуск frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend: `http://localhost:5173`

## API документация

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Основные возможности

- JWT-авторизация пользователей.
- CRUD для пользователей.
- CRUD для публикаций.
- Лента публикаций пользователя с пагинацией.
- Кэширование ленты в Redis (TTL 10 минут).
- Чтение из Postgres с искусственной задержкой при промахе кэша.
- Клиентская лента с модальным просмотром публикации.
- Infinite scroll с автоматической подгрузкой.

## Полезные команды

```bash
# Остановить контейнеры
docker compose down

# Логи backend
docker compose logs -f api

# Production-сборка frontend
cd frontend && npm run build
```
