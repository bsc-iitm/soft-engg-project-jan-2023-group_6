export default ($axios) => ({
  get_faqs(params) {
    return $axios.get('/faq', params)
  },
  update_faq(params) {
    return $axios.put('/faq/update', params)
  },
  create_faq(params) {
    return $axios.post('/faq/create', params)
  },
  delete_faq(faqId) {
    return $axios.delete(`/faq/delete/${faqId}`)
  }
})