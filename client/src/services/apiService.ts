const API_BASE_URL = 'http://localhost:8000'

const pendingRequests = new Map<string, AbortController>()

function pendingRequestKey(path: string, options: RequestInit): string {
  return `${options.method ?? 'GET'} ${path}`
}

function getAbortSignal(path: string, options: RequestInit, abortPreviousRequest: boolean): AbortSignal | undefined {
  if (!abortPreviousRequest) {
    return undefined
  }

  const key = pendingRequestKey(path, options)

  pendingRequests.get(key)?.abort()

  const controller = new AbortController()
  pendingRequests.set(key, controller)

  return controller.signal
}

function clearAbortSignal(path: string, options: RequestInit, signal: AbortSignal | undefined) {
  if (!signal) {
    return
  }

  const key = pendingRequestKey(path, options)

  if (pendingRequests.get(key)?.signal === signal) {
    pendingRequests.delete(key)
  }
}

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

async function request<T>(path: string, options: RequestInit = {}, abortPreviousRequest = true): Promise<T> {
  const token = localStorage.getItem('token')
  const signal = getAbortSignal(path, options, abortPreviousRequest)

  try {
    const response = await fetch(`${API_BASE_URL}${path}`, {
      ...options,
      signal,
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Token ${token}` } : {}),
        ...options.headers,
      },
    })

    return await handleResponse<T>(response)
  } finally {
    clearAbortSignal(path, options, signal)
  }
}

async function requestFormData<T>(path: string, formData: FormData, abortPreviousRequest = true): Promise<T> {
  const token = localStorage.getItem('token')
  const options: RequestInit = { method: 'POST' }
  const signal = getAbortSignal(path, options, abortPreviousRequest)

  try {
    const response = await fetch(`${API_BASE_URL}${path}`, {
      ...options,
      signal,
      headers: (token ? { Authorization: `Token ${token}` } : {}),
      body: formData,
    })

    return await handleResponse<T>(response)
  } finally {
    clearAbortSignal(path, options, signal)
  }
}

export const apiService = {
  list<T>(path: string, abortPreviousRequest = true) {
    return request<T[]>(path, {}, abortPreviousRequest)
  },

  retrieve<T>(path: string, abortPreviousRequest = true) {
    return request<T>(path, {}, abortPreviousRequest)
  },

  post<T>(path: string, body: unknown, abortPreviousRequest = true) {
    return request<T>(
      path,
      {
        method: 'POST',
        body: JSON.stringify(body),
      },
      abortPreviousRequest,
    )
  },

  postFormData<T>(path: string, formData: FormData, abortPreviousRequest = true) {
    return requestFormData<T>(path, formData, abortPreviousRequest)
  },

  delete(path: string, abortPreviousRequest = true) {
    return request<void>(path, { method: 'DELETE' }, abortPreviousRequest)
  },
}
