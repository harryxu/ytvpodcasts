import { create } from "zustand"
import type { DownloadTask, DownloadTaskResponse, Episode } from "./types"

export interface AppStoreInterface {
  playingEpisode?: Episode
  setPlayingEpisode: (episode?: Episode) => void
}

export const useAppStore = create<AppStoreInterface>(set => ({
  playingEpisode: undefined,
  setPlayingEpisode: (episode?: Episode) => set({ playingEpisode: episode }),
}))

export interface TaskStoreInterface {
  notifyCount: number
  tasks: DownloadTask[]
  allowAutoUpdate: boolean
  setTasks: (tasks: DownloadTaskResponse) => void
  setNotifyCount: (count: number) => void
  setAllowAutoUpdate: (allow: boolean) => void
}

const taskInitialState = {
  notifyCount: 0,
  tasks: [],
  allowAutoUpdate: true,
}

export const useTaskStore = create<TaskStoreInterface>(set => ({
  ...taskInitialState,

  setTasks: (tasks: DownloadTaskResponse) =>
    set({ tasks: tasks.data, notifyCount: tasks.notify_count }),

  setNotifyCount: (count: number) => set({ notifyCount: count }),

  setAllowAutoUpdate: (allow: boolean) => set({ allowAutoUpdate: allow }),
}))
