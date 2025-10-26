import { useQuery } from "@tanstack/react-query"
import axios from "axios"
import type { DownloadTaskResponse } from "./types"

const TaskList = () => {
  const tasksQuery = useQuery({
    queryKey: [],
    queryFn: async (): Promise<DownloadTaskResponse> => {
      const res = await axios.get("/api/tasks", {
        params: { page: 1, per_page: 10 },
      })
      return res.data
    },
  })

  return <div>Task List</div>
}

export default TaskList
