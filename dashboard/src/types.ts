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

export interface Pagination {
  page: number
  per_page: number
  total_items: number
  total_pages: number
}

export interface EpisodesResponse {
  data: Episode[]
  pagination: Pagination
}
