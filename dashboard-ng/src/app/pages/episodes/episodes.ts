import {
  Component,
  inject,
  signal,
  computed,
  isDevMode,
} from '@angular/core'
import { HttpClient } from '@angular/common/http'
import { lastValueFrom } from 'rxjs'
import { injectQuery } from '@tanstack/angular-query-experimental'
import { MatCardModule } from '@angular/material/card'
import { MatListModule } from '@angular/material/list'
import { MatPaginatorModule, PageEvent } from '@angular/material/paginator'
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner'
import { LucideAngularModule, Play, AudioLines } from 'lucide-angular'
import { AppStore } from '../../stores'
import type { Episode, EpisodesResponse } from '../../types'
import { EpisodeMetaComponent } from '../../components/episode-meta/episode-meta'

@Component({
  selector: 'app-episodes',
  standalone: true,
  imports: [
    MatCardModule,
    MatListModule,
    MatPaginatorModule,
    MatProgressSpinnerModule,
    LucideAngularModule,
    EpisodeMetaComponent,
  ],
  templateUrl: './episodes.html',
  styleUrl: './episodes.scss',
})
export class EpisodesComponent {
  private http = inject(HttpClient)
  appStore = inject(AppStore)

  readonly PlayIcon = Play
  readonly AudioLinesIcon = AudioLines

  readonly perPage = 8
  currentPage = signal(1)

  episodesQuery = injectQuery(() => ({
    queryKey: ['episodesList', this.currentPage()],
    queryFn: async (): Promise<EpisodesResponse> => {
      const data = await lastValueFrom(
        this.http.get<EpisodesResponse>('/api/episodes', {
          params: { page: this.currentPage(), per_page: this.perPage },
        }),
      )
      if (isDevMode()) {
        return {
          ...data,
          data: [
            {
              id: 'dev-preview',
              title: 'Dev Preview Episode',
              description: 'This is a placeholder episode for development.',
              duration: 3661,
              thumbnail: '',
              audio_file: '',
              audio_file_size: 0,
              audio_file_type: 'audio/mpeg',
              create_date: new Date().toISOString(),
              upload_date: new Date().toISOString(),
              webpage_url: 'https://example.com',
            },
            ...data.data,
          ],
        }
      }
      return data
    },
  }))

  totalItems = computed(() => this.episodesQuery.data()?.pagination.total_items ?? 0)
  totalPages = computed(() => this.episodesQuery.data()?.pagination.total_pages ?? 0)

  isPlaying(episode: Episode): boolean {
    return this.appStore.playingEpisode()?.id === episode.id
  }

  togglePlay(episode: Episode): void {
    if (this.isPlaying(episode)) {
      this.appStore.setPlayingEpisode(undefined)
    } else {
      this.appStore.setPlayingEpisode(episode)
    }
  }

  onPageChange(event: PageEvent): void {
    this.currentPage.set(event.pageIndex + 1)
  }

  formatDuration(seconds: number): string {
    const h = Math.floor(seconds / 3600)
    const m = Math.floor((seconds % 3600) / 60)
    const s = Math.floor(seconds % 60)
    const mm = m.toString().padStart(2, '0')
    const ss = s.toString().padStart(2, '0')
    return h > 0 ? `${h}:${mm}:${ss}` : `${mm}:${ss}`
  }
}
