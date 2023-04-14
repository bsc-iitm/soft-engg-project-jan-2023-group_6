export default ($axios) => ({
  tickets(params) {
    return $axios.get('influencer_count_calc', { params })
  },
})
