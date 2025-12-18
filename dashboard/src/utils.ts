export function isValidUrl(urlStr: string): boolean {
  try {
    const url = new URL(urlStr)
    return url.protocol === "https:"
  } catch (e) {
    return false
  }
}
