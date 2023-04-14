export default ($axios) => ({
  get_faqs(params) {
    return $axios.get('/faq', params)
  },
})