import { Component, signal, inject } from '@angular/core'
import { FormsModule } from '@angular/forms'
import { MatFormFieldModule } from '@angular/material/form-field'
import { MatInputModule } from '@angular/material/input'
import { MatButtonModule } from '@angular/material/button'
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner'
import { HttpClient } from '@angular/common/http'
import {
  injectMutation,
  injectQueryClient,
} from '@tanstack/angular-query-experimental'
import { lastValueFrom } from 'rxjs'
import { NotificationService } from '../../services/notification.service'
import { isValidUrl } from '../../utils'

@Component({
  selector: 'app-cast-input',
  standalone: true,
  imports: [
    FormsModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatProgressSpinnerModule,
  ],
  templateUrl: './cast-input.html',
  styleUrl: './cast-input.scss',
})
export class CastInputComponent {
  private http = inject(HttpClient)
  private notification = inject(NotificationService)
  private queryClient = injectQueryClient()

  videoUrl = signal('')

  mutation = injectMutation(() => ({
    mutationFn: (url: string) =>
      lastValueFrom(this.http.post('/api/add', { url })),
  }))

  async handleAdd(): Promise<void> {
    const url = this.videoUrl().trim()

    if (!isValidUrl(url)) {
      this.notification.error('Video URL must be a valid HTTPS URL')
      return
    }

    try {
      await this.mutation.mutateAsync(url)
      this.videoUrl.set('')
      this.notification.success('Video download task added.')
      await this.queryClient.invalidateQueries({ queryKey: ['tasks'] })
    } catch {
      this.notification.error('Failed to add download task.')
    }
  }

  onKeydown(event: KeyboardEvent): void {
    if (event.key === 'Enter') {
      this.handleAdd()
    }
  }
}
