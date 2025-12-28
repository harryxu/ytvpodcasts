import { useQuery } from "@tanstack/react-query"
import axios from "axios"
import type { DownloadTaskResponse } from "./types"
import { useEffect } from "react"
import { useTaskStore } from "./stores"

export const useDownloadTasksQuery = (enabled: boolean = true) => {
  const { setTasks, allowAutoUpdate } = useTaskStore()
  const tasksQuery = useQuery({
    queryKey: ["tasks"],
    queryFn: async (): Promise<DownloadTaskResponse> => {
      const res = await axios.get("/api/tasks", {
        params: { page: 1, per_page: 10 },
      })
      return res.data
    },
    enabled,
    refetchInterval: allowAutoUpdate ? 300 * 1000 : false,
  })

  useEffect(() => {
    if (!tasksQuery.isFetching && tasksQuery.data) {
      if (import.meta.env.PROD) {
        setTasks(tasksQuery.data)
      } else {
        setTasks({
          ...tasksQuery.data,
          data: [
            {
              title: "Testing task",
              status: "pending",
              created_at: "2025-12-26T16:10:52.737290",
              completed_at: "2025-12-26T16:11:17.173823",
              id: 99999,
              description: null,
              updated_at: "2025-12-26T16:07:29.662624",
              episode_id: null,
            },
            ...tasksQuery.data.data,
          ],
        })
      }
    }
  }, [tasksQuery.isFetching, tasksQuery.data, setTasks])

  return tasksQuery
}
