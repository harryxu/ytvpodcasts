import { useQuery } from "@tanstack/react-query"
import axios from "axios"
import type { DownloadTaskResponse } from "./types"
import { useEffect } from "react"
import { useTaskStore } from "./stores"

export const useDownloadTasksQuery = () => {
  const taskStore = useTaskStore()
  const tasksQuery = useQuery({
    queryKey: ["tasks"],
    queryFn: async (): Promise<DownloadTaskResponse> => {
      const res = await axios.get("/api/tasks", {
        params: { page: 1, per_page: 10 },
      })
      return res.data
    },
    enabled: false,
  })

  useEffect(() => {
    if (!tasksQuery.isFetching && tasksQuery.data) {
      taskStore.setTasks(tasksQuery.data)
    }
  }, [tasksQuery.isFetching, tasksQuery.data, taskStore])

  return tasksQuery
}
