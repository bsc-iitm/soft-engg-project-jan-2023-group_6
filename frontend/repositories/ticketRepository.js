export default ($axios) => ({
  getTickets(params) {
    return $axios.get('/user/tickets', { params })
  },
})
