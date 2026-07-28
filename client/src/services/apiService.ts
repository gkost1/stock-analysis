const API_BASE_URL = 'http://localhost:8000'

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const data = await response.json().catch(() => ({}))
    throw new Error(data.detail ?? 'Something went wrong. Please try again.')
  }

  if (response.status === 204) {
    return undefined as T
  }

  return response.json()
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = localStorage.getItem('token')

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Token ${token}` } : {}),
      ...options.headers,
    },
  })

  return handleResponse<T>(response)
}

async function requestFormData<T>(path: string, formData: FormData): Promise<T> {
  const token = localStorage.getItem('token')

  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: 'POST',
    headers: {
      ...(token ? { Authorization: `Token ${token}` } : {}),
    },
    body: formData,
  })

  return handleResponse<T>(response)
}

export const apiService = {
  list<T>(path: string) {
    return request<T[]>(path)
  },

  retrieve<T>(path: string) {
    return request<T>(path)
  },

  post<T>(path: string, body: unknown) {
    return request<T>(path, {
      method: 'POST',
      body: JSON.stringify(body),
    })
  },

  postFormData<T>(path: string, formData: FormData) {
    return requestFormData<T>(path, formData)
  },

  delete(path: string) {
    return request<void>(path, { method: 'DELETE' })
  },
}
