import { Component, inject, DestroyRef, effect, isDevMode } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { injectQuery } from '@tanstack/angular-query-experimental';
import { lastValueFrom } from 'rxjs';
import { MatCardModule } from '@angular/material/card';
import { MatListModule } from '@angular/material/list';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { LucideAngularModule, RefreshCcw, CircleCheck, CircleX } from 'lucide-angular';
import { TaskStore } from '../../stores';
import type { DownloadTaskResponse, DownloadTask } from '../../types';

@Component({
  selector: 'app-tasks',
  standalone: true,
  imports: [MatCardModule, MatListModule, MatButtonModule, MatProgressSpinnerModule, LucideAngularModule],
  templateUrl: './tasks.html',
  styleUrl: './tasks.scss',
})
export class TasksComponent {
  private http = inject(HttpClient);
  taskStore = inject(TaskStore);

  readonly RefreshCcwIcon = RefreshCcw;
  readonly CircleCheckIcon = CircleCheck;
  readonly CircleXIcon = CircleX;

  tasksQuery = injectQuery(() => ({
    queryKey: ['tasks'],
    queryFn: () =>
      lastValueFrom(
        this.http.get<DownloadTaskResponse>('/api/tasks', {
          params: { page: 1, per_page: 10 },
        }),
      ),
    refetchInterval: this.taskStore.allowAutoUpdate() ? 300 * 1000 : false,
  }));

  constructor() {
    const destroyRef = inject(DestroyRef);

    // Disable auto-update while on the tasks page
    this.taskStore.setAllowAutoUpdate(false);
    destroyRef.onDestroy(() => this.taskStore.setAllowAutoUpdate(true));

    // Sync query results to the TaskStore
    effect(() => {
      const data = this.tasksQuery.data();
      const isFetching = this.tasksQuery.isFetching();
      if (!isFetching && data) {
        if (!isDevMode()) {
          this.taskStore.setTasks(data);
        } else {
          this.taskStore.setTasks({
            ...data,
            data: [
              {
                title: 'Testing task',
                status: 'pending',
                created_at: '2025-12-26T16:10:52.737290',
                completed_at: '2025-12-26T16:11:17.173823',
                id: 99999,
                description: null,
                updated_at: '2025-12-26T16:07:29.662624',
                episode_id: null,
              },
              ...data.data,
            ],
          });
        }
      }
    });
  }

  refetch(): void {
    this.tasksQuery.refetch();
  }

  taskStatus(task: DownloadTask): 'success' | 'failed' | 'progress' {
    if (task.status === 'success') return 'success';
    if (task.status === 'failed') return 'failed';
    return 'progress';
  }

  progressValue(task: DownloadTask): number | undefined {
    return task.progress ? task.progress._percent : undefined;
  }
}
