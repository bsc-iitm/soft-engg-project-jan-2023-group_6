export default ($axios) => ({
  get_faqs(params) {
    return $axios.get('/faq', params)
  },
  update_faq(params) {
    return $axios.put('/faq', params)
  }
})