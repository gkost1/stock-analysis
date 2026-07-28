import { apiService } from './apiService'

export type PortfolioViewYAxis = 'value' | 'profit_loss' | 'cagr'

export interface PortfolioView {
  id: number
  portfolio: number
  asset: string | null
  x_axis: string
  y_axis: PortfolioViewYAxis
}

export interface CreatePortfolioViewPayload {
  portfolio: number
  asset: string | null
  x_axis: string
  y_axis: PortfolioViewYAxis
}

export interface PerformancePoint {
  date: string
  value: string
  profit_loss: string
  cagr: string | null
}

const BASE_PATH = '/simulations/portfolio_views/'

export const portfolioViewsService = {
  create(payload: CreatePortfolioViewPayload) {
    return apiService.post<PortfolioView>(BASE_PATH, payload)
  },
  delete(viewId: number) {
    return apiService.delete(`${BASE_PATH}${viewId}/`)
  },
  performance(viewId: number) {
    return apiService.list<PerformancePoint>(`${BASE_PATH}${viewId}/performance/`)
  },
}
