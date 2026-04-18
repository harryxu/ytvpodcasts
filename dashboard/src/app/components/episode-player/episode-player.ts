import { Component, inject, signal, effect, viewChild, ElementRef } from '@angular/core'
import { MatIconButton } from '@angular/material/button'
import { LucideAngularModule, X } from 'lucide-angular'
import { AppStore } from '../../stores'

@Component({
  selector: 'app-episode-player',
  standalone: true,
  imports: [MatIconButton, LucideAngularModule],
  templateUrl: './episode-player.html',
  styleUrl: './episode-player.scss',
})
export class EpisodePlayerComponent {
  appStore = inject(AppStore)

  readonly XIcon = X

  /** Keep player visible during slide-out transition */
  playerVisible = signal(false)

  audioEl = viewChild<ElementRef<HTMLAudioElement>>('audioRef')

  constructor() {
    effect(() => {
      const episode = this.appStore.playingEpisode()
      if (!episode) {
        this.audioEl()?.nativeElement.pause()
      }
    })
  }

  onTransitionEnd(): void {
    this.playerVisible.set(!!this.appStore.playingEpisode())
  }

  close(): void {
    this.appStore.setPlayingEpisode(undefined)
  }
}
