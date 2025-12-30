import { describe, expect, it } from "vitest"
import { isValidUrl } from "../utils"

describe("isVideoWatchUrl", () => {
  it("should return true for valid video watch URLs", () => {
    expect(isValidUrl("https://www.youtube.com/watch?v=dQw4w9WgXcQ")).toBe(true)
    expect(isValidUrl("https://youtube.com/watch?v=dQw4w9WgXcQ")).toBe(true)
  })

  it("should return true for valid youtu.be URLs", () => {
    expect(isValidUrl("https://youtu.be/dQw4w9WgXcQ")).toBe(true)
  })

  it("should return true for URLs with extra query parameters", () => {
    expect(isValidUrl("https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=1s")).toBe(
      true
    )
  })

  it("should return true for URLs with extra query parameters", () => {
    expect(
      isValidUrl(
        "https://www.youtube.com/watch?si=2XTjnM2cff5ZJv1J&v=4zyZ3sw_ulc&feature=youtu.be"
      )
    ).toBe(true)
  })

  it("should return false for non-video URLs", () => {
    expect(isValidUrl("https://www.google.com")).toBe(false)
    expect(isValidUrl("https://vimeo.com/12345678")).toBe(false)
  })

  it("should return false for URLs that are not watch or short URLs", () => {
    expect(isValidUrl("https://www.youtube.com/c/SomeChannel")).toBe(false)
    expect(isValidUrl("https://www.youtube.com/feed/subscriptions")).toBe(false)
  })

  it("should return false for http URLs", () => {
    expect(isValidUrl("http://www.youtube.com/watch?v=dQw4w9WgXcQ")).toBe(false)
  })

  it("should return false for random strings", () => {
    expect(isValidUrl("not a url")).toBe(false)
    expect(isValidUrl("")).toBe(false)
  })
})
