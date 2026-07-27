export function uniqueUsername() {
  return `user_${Date.now()}_${Math.floor(Math.random() * 100000)}`
}
