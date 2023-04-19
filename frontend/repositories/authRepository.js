export default ($axios) => ({
  login(params) {
    return $axios.post('/login', params)
  },
  signup(params) {
    return $axios.post('/signup', params)
  },
})
