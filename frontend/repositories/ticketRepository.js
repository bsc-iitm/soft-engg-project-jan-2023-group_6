export default ($axios) => ({
  getTickets(params) {
    return $axios.get('/user/tickets', { params })
  },
  getTicket(params) {
    return $axios.get('/user/ticket', { params })
  },
  createTicket(params) {
    return $axios.post('/ticket', params)
  },
  replyTicket(params) {
    return $axios.post('/ticket/reply', params)
  },
})
