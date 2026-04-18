import { Injectable, inject, OnDestroy } from '@angular/core'
import { TaskStore } from '../stores'
import { NotificationService } from './notification.service'
import type { DownloadTask } from '../types'

@Injectable({ providedIn: 'root' })
export class EventStreamService implements OnDestroy {
  private taskStore = inject(TaskStore)
  private notification = inject(NotificationService)
  private es: EventSource | null = null

  connect(): void {
    if (this.es) return

    const es = new EventSource('/api/eventstream')
    this.es = es

    es.onmessage = event => {
      try {
        const data = JSON.parse(event.data)
        switch (data.type) {
          case 'task': {
            const task: DownloadTask = { ...data.task }
            if (data.progress) {
              task.progress = { ...data.progress }
            }
            this.taskStore.updateTask(task)
            switch (task.status) {
              case 'success':
                this.notification.success(`${task.title} downloaded successfully.`)
                break
              case 'failed':
                this.notification.error(task.description ?? 'Download failed.')
                break
            }
            console.log(
              'Updated task:',
              task.progress?._percent,
              task.progress?._percent_str,
              task,
            )
            break
          }
        }
      } catch (err) {
        console.error('Failed to parse stream data:', err)
      }
    }

    es.onerror = error => {
      console.error('Streaming error:', error)
      es.close()
      this.es = null
    }
  }

  disconnect(): void {
    this.es?.close()
    this.es = null
  }

  ngOnDestroy(): void {
    this.disconnect()
  }
}
