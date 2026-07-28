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

const BASE_PATH = '/simulations/portfolio_holdings/'

export const portfolioHoldingsService = {
  list(portfolioId: number, ticker?: string) {
    const params = new URLSearchParams({ portfolio: String(portfolioId) })
    if (ticker) params.set('ticker', ticker)
    return apiService.list<PortfolioHolding>(`${BASE_PATH}?${params}`)
  },

  create(portfolioId: number, payload: CreatePortfolioHoldingPayload) {
    return apiService.post<PortfolioHolding>(BASE_PATH, { ...payload, portfolio: portfolioId })
  },

  uploadCsv(portfolioId: number, source: string, file: File) {
    const formData = new FormData()
    formData.append('portfolio', String(portfolioId))
    formData.append('source', source)
    formData.append('file', file)
    return apiService.postFormData<PortfolioHolding[]>(`${BASE_PATH}upload/`, formData)
  },
}
