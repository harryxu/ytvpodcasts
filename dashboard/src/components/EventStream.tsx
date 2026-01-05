import { useEffect, useRef } from "react"
import { useTaskStore } from "../stores"
import type { DownloadTask } from "../types"

export default function EventStream() {
  const esRef = useRef<EventSource | null>(null)
  const taskStore = useTaskStore()

  useEffect(() => {
    if (esRef.current) return

    const es = new EventSource("/api/eventstream")
    esRef.current = es

    es.onmessage = event => {
      try {
        const data = JSON.parse(event.data)
        switch (data.type) {
          case "task":
            const task: DownloadTask = { ...data.task }
            if (data.progress) {
              task.progress = { ...data.progress }
            }
            taskStore.updateTask(task)
            console.log(
              "Updated task:",
              task.progress?._percent,
              task.progress?._percent_str,
              task
            )
            break
        }
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
