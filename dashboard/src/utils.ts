export function isYouTubeWatchUrl(url: string): boolean {
  const regex = /^https:\/\/(www\.)?youtube\.com\/watch\?v=|https:\/\/youtu\.be\//

  return regex.test(url)
}
