export function isYouTubeWatchUrl(url: string): boolean {
  // First check if it's a youtu.be URL
  if (url.startsWith("https://youtu.be/")) {
    return true
  }

  // Then check if it's a youtube.com/watch URL with v= parameter
  const youtubeWatchRegex = /^https:\/\/(www\.)?youtube\.com\/watch\?/
  if (!youtubeWatchRegex.test(url)) {
    return false
  }

  // Extract query parameters and check for v= parameter
  const urlObj = new URL(url)
  return urlObj.searchParams.has("v")
}
