export default ($axios) => ({
  getTickets(params) {
    return $axios.get('/user/tickets', { params })
  },
  createTicket(params) {
    return $axios.post('/ticket', params)
  },
})
