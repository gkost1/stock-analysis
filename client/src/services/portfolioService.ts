import { apiService } from './apiService'
import type { PortfolioView } from './portfolioViewsService'

export interface Portfolio {
  id: number
  title: string
  start_date: string
  end_date: string
  created_by: number
  created_at: string
  initial_investment: string
  holdings_count: number
  views: PortfolioView[]
}

export interface CreatePortfolioPayload {
  title: string
  start_date: string
  end_date: string
}

const BASE_PATH = '/simulations/portfolios/'

export const portfolioService = {
  create(payload: CreatePortfolioPayload) {
    return apiService.post<Portfolio>(BASE_PATH, payload)
  },
  retrieve(id: number) {
    return apiService.retrieve<Portfolio>(`${BASE_PATH}${id}/`)
  },
  list() {
    return apiService.list<Portfolio>(BASE_PATH)
  },
}
