import { apiService } from './apiService'

export type StudyViewYAxis = 'value' | 'profit_loss' | 'cagr'

export interface StudyView {
  id: number
  study: number
  asset: string | null
  x_axis: string
  y_axis: StudyViewYAxis
}

export interface CreateStudyViewPayload {
  study: number
  asset: string | null
  x_axis: string
  y_axis: StudyViewYAxis
}

export interface PerformancePoint {
  date: string
  value: string
  profit_loss: string
  cagr: string | null
}

const BASE_PATH = '/simulations/study_views/'

export const studyViewsService = {
  create(payload: CreateStudyViewPayload) {
    return apiService.post<StudyView>(BASE_PATH, payload)
  },

  delete(viewId: number) {
    return apiService.delete(`${BASE_PATH}${viewId}/`)
  },

  performance(viewId: number) {
    return apiService.list<PerformancePoint>(`${BASE_PATH}${viewId}/performance/`)
  },
}
