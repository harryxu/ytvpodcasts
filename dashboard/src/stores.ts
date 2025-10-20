import { create } from "zustand"

export interface TaskStoreInterface {
  notifyCount: number
}

export const useTaskStore = create<TaskStoreInterface>(set => ({
  notifyCount: 0,

  setNotifyCount: (count: number) => set({ notifyCount: count }),
}))
