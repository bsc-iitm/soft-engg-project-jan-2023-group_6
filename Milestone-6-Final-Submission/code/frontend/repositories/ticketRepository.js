export default ($axios) => ({
  getTickets(params) {
    return $axios.get(
      '/user/tickets',
      { params },
      {
        headers: {
          Authorization: 'abc',
        },
      }
    )
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
  markAsSolved(params) {
    return $axios.post('/ticket/mark_solved', params)
  },
  likeTicket(params) {
    return $axios.post('/ticket/mark_solved', params)
  },
})
