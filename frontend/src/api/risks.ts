import api from './request'

export const riskApi = {
  list(contractId: number) { return api.get(`/contracts/${contractId}/risks`) },
  updateStatus(contractId: number, riskId: number, status: string) {
    return api.put(`/contracts/${contractId}/risks/${riskId}/status`, { status })
  },
}
