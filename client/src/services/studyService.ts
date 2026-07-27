import { apiService } from './apiService'

export interface Study {
  id: number
  title: string
  start_date: string
  end_date: string
  created_by: number
  created_at: string
}

export interface CreateStudyPayload {
  title: string
  start_date: string
  end_date: string
}

const BASE_PATH = '/simulations/studies/'

export const studyService = {
  create(payload: CreateStudyPayload) {
    return apiService.post<Study>(BASE_PATH, payload)
  },

  retrieve(id: number) {
    return apiService.retrieve<Study>(`${BASE_PATH}${id}/`)
  },

  list() {
    return apiService.list<Study>(BASE_PATH)
  },
}
