import { useEffect, useRef } from "react"
import { useDownloadTasksQuery } from "../api"
import axios, { type AxiosResponse } from "axios"

export default function TaskUpdater() {
  const abortControllerRef = useRef<AbortController | null>(null)
  const responseRef = useRef<AxiosResponse | null>(null)

  const esRef = useRef<EventSource | null>(null)

  useEffect(() => {
    if (esRef.current) return

    const es = new EventSource("/api/eventstream", { withCredentials: true })
    esRef.current = es

    es.onmessage = event => {
      try {
        const data = JSON.parse(event.data)
        console.log("收到消息:", data)
      } catch (err) {
        console.error("解析失败:", err)
      }
    }

    es.onerror = err => {
      console.error("流错误:", err)
      es.close()
    }

    return () => {
      es.close()
      esRef.current = null
    }
  }, [])

  return null
}
