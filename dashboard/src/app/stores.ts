import { Injectable, signal } from '@angular/core'
import type { DownloadTask, DownloadTaskResponse, Episode } from './types'

@Injectable({ providedIn: 'root' })
export class AppStore {
  private readonly _playingEpisode = signal<Episode | undefined>(undefined)

  readonly playingEpisode = this._playingEpisode.asReadonly()

  setPlayingEpisode(episode?: Episode): void {
    this._playingEpisode.set(episode)
  }
}

@Injectable({ providedIn: 'root' })
export class TaskStore {
  private readonly _notifyCount = signal<number>(0)
  private readonly _tasks = signal<DownloadTask[]>([])
  private readonly _allowAutoUpdate = signal<boolean>(true)

  readonly notifyCount = this._notifyCount.asReadonly()
  readonly tasks = this._tasks.asReadonly()
  readonly allowAutoUpdate = this._allowAutoUpdate.asReadonly()

  setTasks(response: DownloadTaskResponse): void {
    this._tasks.set(response.data)
    this._notifyCount.set(response.notify_count)
  }

  updateTask(task: DownloadTask): void {
    this._tasks.update(tasks => tasks.map(t => (t.id === task.id ? task : t)))
  }

  setNotifyCount(count: number): void {
    this._notifyCount.set(count)
  }

  setAllowAutoUpdate(allow: boolean): void {
    this._allowAutoUpdate.set(allow)
  }
}
