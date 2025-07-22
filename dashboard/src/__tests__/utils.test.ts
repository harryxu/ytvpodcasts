import { describe, expect, it } from "vitest"
import { isYouTubeWatchUrl } from "../utils"

describe("isYouTubeWatchUrl", () => {
  it("should return true for valid youtube.com watch URLs", () => {
    expect(
      isYouTubeWatchUrl("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    ).toBe(true)
    expect(isYouTubeWatchUrl("https://youtube.com/watch?v=dQw4w9WgXcQ")).toBe(
      true
    )
  })

  it("should return true for valid youtu.be URLs", () => {
    expect(isYouTubeWatchUrl("https://youtu.be/dQw4w9WgXcQ")).toBe(true)
  })

  it("should return true for URLs with extra query parameters", () => {
    expect(
      isYouTubeWatchUrl("https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=1s")
    ).toBe(true)
  })

  it("should return false for non-youtube URLs", () => {
    expect(isYouTubeWatchUrl("https://www.google.com")).toBe(false)
    expect(isYouTubeWatchUrl("https://vimeo.com/12345678")).toBe(false)
  })

  it("should return false for URLs that are not watch or short URLs", () => {
    expect(isYouTubeWatchUrl("https://www.youtube.com/c/SomeChannel")).toBe(
      false
    )
    expect(
      isYouTubeWatchUrl("https://www.youtube.com/feed/subscriptions")
    ).toBe(false)
  })

  it("should return false for http URLs", () => {
    expect(
      isYouTubeWatchUrl("http://www.youtube.com/watch?v=dQw4w9WgXcQ")
    ).toBe(false)
  })

  it("should return false for random strings", () => {
    expect(isYouTubeWatchUrl("not a url")).toBe(false)
    expect(isYouTubeWatchUrl("")).toBe(false)
  })
})
