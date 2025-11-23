import { create } from "zustand"
import type { DownloadTask, DownloadTaskResponse } from "./types"

export interface TaskStoreInterface {
  notifyCount: number
  tasks: DownloadTask[]
  allowAutoUpdate: boolean
  setTasks: (tasks: DownloadTaskResponse) => void
  setNotifyCount: (count: number) => void
  setAllowAutoUpdate: (allow: boolean) => void
}

const initialState = {
  notifyCount: 0,
  tasks: [],
  allowAutoUpdate: true,
}

export const useTaskStore = create<TaskStoreInterface>(set => ({
  ...initialState,

  setTasks: (tasks: DownloadTaskResponse) =>
    set({ tasks: tasks.data, notifyCount: tasks.notify_count }),

  setNotifyCount: (count: number) => set({ notifyCount: count }),

  setAllowAutoUpdate: (allow: boolean) => set({ allowAutoUpdate: allow }),
}))
