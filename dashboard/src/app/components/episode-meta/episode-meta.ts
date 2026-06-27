import { ChangeDetectionStrategy, Component, computed, inject, input } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { injectMutation, QueryClient } from '@tanstack/angular-query-experimental';
import { lastValueFrom } from 'rxjs';
import { MatIconButton } from '@angular/material/button';
import { MatMenuModule } from '@angular/material/menu';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { LucideAngularModule, Ellipsis, Archive, ArchiveRestore, Trash, Clock } from 'lucide-angular';
import { NotificationService } from '../../services/notification.service';
import type { Episode } from '../../types';

@Component({
  selector: 'app-episode-meta',
  imports: [MatIconButton, MatMenuModule, MatProgressSpinnerModule, LucideAngularModule],
  templateUrl: './episode-meta.html',
  styleUrl: './episode-meta.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class EpisodeMetaComponent {
  episode = input.required<Episode>();

  private http = inject(HttpClient);
  private notification = inject(NotificationService);
  private queryClient = inject(QueryClient);

  readonly EllipsisIcon = Ellipsis;
  readonly ArchiveIcon = Archive;
  readonly ArchiveRestoreIcon = ArchiveRestore;
  readonly TrashIcon = Trash;
  readonly ClockIcon = Clock;

  archiveMutation = injectMutation(() => ({
    mutationFn: () => lastValueFrom(this.http.post(`/api/episodes/${this.episode().id}/archive`, {})),
    onSuccess: () => {
      this.queryClient.invalidateQueries({ queryKey: ['episodesList'] });
      this.notification.success('Episode has been archived.');
    },
  }));

  unarchiveMutation = injectMutation(() => ({
    mutationFn: () => lastValueFrom(this.http.post(`/api/episodes/${this.episode().id}/unarchive`, {})),
    onSuccess: () => {
      this.queryClient.invalidateQueries({ queryKey: ['episodesList'] });
      this.notification.success('Episode has been unarchived.');
    },
  }));

  deleteMutation = injectMutation(() => ({
    mutationFn: () => lastValueFrom(this.http.delete(`/api/episodes/${this.episode().id}`)),
    onSuccess: () => {
      this.queryClient.invalidateQueries({ queryKey: ['episodesList'] });
      this.notification.success('Episode has been deleted.');
    },
  }));

  isPending = computed(
    () =>
      this.archiveMutation.isPending() ||
      this.unarchiveMutation.isPending() ||
      this.deleteMutation.isPending(),
  );

  isArchived = computed(() => this.episode().is_archived);

  get duration(): { hours: number; minutes: number; seconds: number } {
    const d = this.episode().duration;
    return {
      hours: Math.floor(d / 3600),
      minutes: Math.floor((d % 3600) / 60),
      seconds: Math.floor(d % 60),
    };
  }

  archiveEpisode(): void {
    this.archiveMutation.mutate();
  }

  unarchiveEpisode(): void {
    this.unarchiveMutation.mutate();
  }

  deleteEpisode(): void {
    if (window.confirm('Are you sure you want to delete this episode? This action cannot be undone.')) {
      this.deleteMutation.mutate();
    }
  }
}
