export const JWT_STORAGE_KEY = 'trendsee.jwt'

export function getJwtToken(): string | null {
  try {
    return localStorage.getItem(JWT_STORAGE_KEY)
  } catch {
    return null
  }
}

