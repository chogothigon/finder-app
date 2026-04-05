import { reactive } from 'vue'
 
const state = reactive({
  favorites: new Set(),   // Set of car_id strings
  user: null,             // { id, name, email, avatar } or null
  loaded: false
})
 
async function fetchUser() {
  try {
    const res = await fetch('/api/v1/auth/me', { credentials: 'include' })
    state.user = res.ok ? await res.json() : null
  } catch {
    state.user = null
  }
}
 
function loadFromLocalStorage() {
  try {
    const raw = localStorage.getItem('favorites')
    const ids = raw ? JSON.parse(raw) : []
    state.favorites = new Set(ids.map(String))
  } catch {
    state.favorites = new Set()
  }
}
 
function saveToLocalStorage() {
  localStorage.setItem('favorites', JSON.stringify([...state.favorites]))
}
 
async function loadFromDB() {
  try {
    const res = await fetch('/api/favorites', { credentials: 'include' })
    if (res.ok) {
      const ids = await res.json()
      state.favorites = new Set(ids.map(String))
    }
  } catch (e) {
    console.error('Failed to load favorites from DB:', e)
  }
}
 
async function syncLocalStorageToDB() {
  const localIds = [...state.favorites]
  if (!localIds.length) return
  try {
    await fetch('/api/favorites/sync', {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ car_ids: localIds })
    })
    localStorage.removeItem('favorites')
  } catch (e) {
    console.error('Failed to sync favorites:', e)
  }
}
 
export async function initFavorites() {
  if (state.loaded) return
  state.loaded = true
 
  await fetchUser()
 
  if (state.user) {
    loadFromLocalStorage()
    if (state.favorites.size > 0) await syncLocalStorageToDB()
    await loadFromDB()
  } else {
    loadFromLocalStorage()
  }
}
 
export function isFavorited(carId) {
  return state.favorites.has(String(carId))
}
 
export async function toggleFavorite(carId) {
  const id = String(carId)
  const adding = !state.favorites.has(id)

  const next = new Set(state.favorites)
  if (adding) next.add(id)
  else next.delete(id)
  state.favorites = next
 
  if (state.user) {
    try {
      if (adding) {
        await fetch('/api/favorites', {
          method: 'POST',
          credentials: 'include',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ car_id: carId })
        })
      } else {
        await fetch(`/api/favorites/${carId}`, {
          method: 'DELETE',
          credentials: 'include'
        })
      }
    } catch (e) {
      // Rollback on failure
      const rollback = new Set(state.favorites)
      if (adding) rollback.delete(id)
      else rollback.add(id)
      state.favorites = rollback
      console.error('Failed to update favorite:', e)
    }
  } else {
    saveToLocalStorage()
  }
}
 
export { state as favoritesState }
 