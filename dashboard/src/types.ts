export interface Pagination {
  page: number
  per_page: number
  total_items: number
  total_pages: number
}

export interface Episode {
  audio_file: string
  audio_file_size: number
  audio_file_type: string
  create_date: string
  description: string
  duration: number
  id: string
  thumbnail: string
  title: string
  upload_date: string
  webpage_url: string
}

export interface EpisodesResponse {
  data: Episode[]
  pagination: Pagination
}

export interface DownloadTask {
  completed_at: string | null
  created_at: string
  description: string | null
  episode_id: string | null
  id: number
  status: string
  title: string
  updated_at: string
}

export interface DownloadTaskResponse {
  data: DownloadTask[]
  notify_count: number
  pagination: Pagination
}
