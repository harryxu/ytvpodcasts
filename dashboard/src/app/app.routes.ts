import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () => import('./pages/episodes/episodes').then((m) => m.EpisodesComponent),
  },
  {
    path: 'tasks',
    loadComponent: () => import('./pages/tasks/tasks').then((m) => m.TasksComponent),
  },
  {
    path: '**',
    redirectTo: '',
  },
];
