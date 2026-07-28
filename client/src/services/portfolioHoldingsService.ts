import { apiService } from './apiService'

export interface PortfolioHolding {
  id: number
  portfolio: number
  ticker: string
  quantity: string
  cost_per_share: string
  date_purchased: string
  date_sold: string | null
  current_share_price: string | null
  total_cost: string
  total_value: string | null
  profit_loss: string | null
}

export interface CreatePortfolioHoldingPayload {
  ticker: string
  quantity: string
  cost_per_share: string
  date_purchased: string
  date_sold?: string | null
}

export const portfolioHoldingsService = {
  list(studyId: number) {
    return apiService.list<PortfolioHolding>(`/simulations/studies/${studyId}/holdings/`)
  },

  create(studyId: number, payload: CreatePortfolioHoldingPayload) {
    return apiService.post<PortfolioHolding>(
      `/simulations/studies/${studyId}/holdings/`,
      payload,
    )
  },

  uploadCsv(studyId: number, source: string, file: File) {
    const formData = new FormData()
    formData.append('source', source)
    formData.append('file', file)
    return apiService.postFormData<PortfolioHolding[]>(
      `/simulations/studies/${studyId}/holdings/upload/`,
      formData,
    )
  },
}
