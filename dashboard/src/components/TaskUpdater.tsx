import { useEffect, useRef } from "react"
import { useDownloadTasksQuery } from "../api"
import axios, { type AxiosResponse } from "axios"

export default function TaskUpdater() {
  // const taskQuery = useDownloadTasksQuery()

  const abortControllerRef = useRef<AbortController | null>(null)
  const responseRef = useRef<AxiosResponse | null>(null)

  const startStream = async () => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort()
    }

    abortControllerRef.current = new AbortController()
    responseRef.current = await axios.get("/api/eventstream", {
      responseType: "json",
      signal: abortControllerRef.current.signal,
    })
    if (!responseRef.current) {
      return
    }

    const stream = responseRef.current.data

    stream.on("data", data => {
      console.log("stream data ------", data)
    })

    stream.on("end", () => {
      console.log("stream done")
    })

    stream.on("error", (err: any) => {
      if (axios.isCancel(err)) {
        console.log("用户手动断开了流")
      } else {
        console.error("流发生错误", err)
      }
    })
  }

  useEffect(() => {
    if (!responseRef.current) {
      console.log("no streaming")
      startStream()
    }

    return () => {
      if (abortControllerRef.current) {
        abortControllerRef.current.abort()
        abortControllerRef.current = null
      }
    }
  }, [])

  return null
}
