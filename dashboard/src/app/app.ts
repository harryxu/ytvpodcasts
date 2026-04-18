import { Component, inject, OnInit } from '@angular/core';
import { RouterOutlet, RouterLink, RouterLinkActive } from '@angular/router';
import { MatTabsModule } from '@angular/material/tabs';
import { LucideAngularModule, Rss } from 'lucide-angular';
import { CastInputComponent } from './components/cast-input/cast-input';
import { EpisodePlayerComponent } from './components/episode-player/episode-player';
import { EventStreamService } from './services/event-stream.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    RouterOutlet,
    RouterLink,
    RouterLinkActive,
    MatTabsModule,
    LucideAngularModule,
    CastInputComponent,
    EpisodePlayerComponent,
  ],
  templateUrl: './app.html',
  styleUrl: './app.scss',
})
export class App implements OnInit {
  private eventStream = inject(EventStreamService);

  readonly RssIcon = Rss;

  ngOnInit(): void {
    this.eventStream.connect();
  }
}
