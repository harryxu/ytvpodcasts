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
  updateTask: (task: DownloadTask) => void
  setNotifyCount: (count: number) => void
  setAllowAutoUpdate: (allow: boolean) => void
}

const taskInitialState = {
  notifyCount: 0,
  tasks: [],
  allowAutoUpdate: true,
}

export const useTaskStore = create<TaskStoreInterface>((set, get) => ({
  ...taskInitialState,

  setTasks: (tasks: DownloadTaskResponse) =>
    set({ tasks: tasks.data, notifyCount: tasks.notify_count }),

  updateTask: (task: DownloadTask) =>
    set(state => {
      return { tasks: state.tasks.map(t => (t.id === task.id ? task : t)) }
    }),

  setNotifyCount: (count: number) => set({ notifyCount: count }),

  setAllowAutoUpdate: (allow: boolean) => set({ allowAutoUpdate: allow }),
}))
