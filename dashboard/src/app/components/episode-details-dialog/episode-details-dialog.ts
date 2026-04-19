import { CommonModule, DatePipe } from '@angular/common'
import { Component, inject } from '@angular/core'
import { MAT_DIALOG_DATA, MatDialogModule } from '@angular/material/dialog'
import { MatButtonModule } from '@angular/material/button'
import type { Episode } from '../../types'

@Component({
  selector: 'app-episode-details-dialog',
  standalone: true,
  imports: [CommonModule, DatePipe, MatDialogModule, MatButtonModule],
  templateUrl: './episode-details-dialog.html',
  styleUrl: './episode-details-dialog.scss',
})
export class EpisodeDetailsDialogComponent {
  readonly episode = inject<Episode>(MAT_DIALOG_DATA)

  formatDuration(seconds: number): string {
    const h = Math.floor(seconds / 3600)
    const m = Math.floor((seconds % 3600) / 60)
    const s = Math.floor(seconds % 60)
    const mm = m.toString().padStart(2, '0')
    const ss = s.toString().padStart(2, '0')
    return h > 0 ? `${h}:${mm}:${ss}` : `${mm}:${ss}`
  }
}
