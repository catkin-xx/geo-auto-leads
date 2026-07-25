import axios from 'axios'

const api = axios.create({
    baseURL: '/api',
    timeout: 10000
})

export function getLeads(params) {
    return api.get('/leads/', { params })
}

export function batchScore() {
    return api.post('/leads/batch-score')
}

export function batchOutreach(ids) {
    return api.post('/leads/batch-outreach', ids)
}

export default api