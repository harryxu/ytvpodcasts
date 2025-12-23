import { useEffect, useRef } from "react"

export default function EventStream() {
  const esRef = useRef<EventSource | null>(null)

  useEffect(() => {
    if (esRef.current) return

    const es = new EventSource("/api/eventstream")
    esRef.current = es

    es.onmessage = event => {
      try {
        const data = JSON.parse(event.data)
        console.log("Received stream data:", data)
      } catch (err) {
        console.error("Failed to parse stream data:", err)
      }
    }

    es.onerror = error => {
      console.error("Streaming error:", error)
      es.close()
    }

    return () => {
      es.close()
      esRef.current = null
    }
  }, [])

  return null
}
