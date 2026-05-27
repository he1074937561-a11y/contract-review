import api from './request'

export const contractApi = {
  list(params?: any) { return api.get('/contracts', { params }) },
  get(id: number) { return api.get(`/contracts/${id}`) },
  upload(form: FormData) { return api.post('/contracts/upload', form) },
  delete(id: number) { return api.delete(`/contracts/${id}`) },
}
