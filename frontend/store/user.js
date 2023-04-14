export const state = () => ({
  loggedIn: false,
  userInfo: {},
})

export const actions = {
  setFilters({ commit, dispatch, state }, payload) {
    commit('UPDATE_FILTERS', payload)

    dispatch('formatFilters', state.filterData)

    dispatch('setChicklets', payload)

    dispatch('resetInfluencerList', payload)
  },
  setChicklets({ commit }, payload) {
    let chicklets = ''
    for (const key of Object.keys(payload)) {
      if (payload[key] && payload[key].length) {
        chicklets += payload[key].toString()
        chicklets += ','
      }
    }
    if (chicklets.length) {
      chicklets = chicklets.slice(0, -1)
      chicklets = chicklets.split(',')
    }
    commit('UPDATE_CHICKLETS', chicklets)
  },
  removeChicklets({ dispatch, state }, index) {
    const newChicklets = JSON.parse(JSON.stringify(state.filterChicklets))
    const filters = JSON.parse(JSON.stringify(state.filterData))
    const removedItem = newChicklets.splice(index, 1)
    for (const key of Object.keys(filters)) {
      Array.isArray(filters[key]) &&
        console.log(filters[key].filter((node) => node === removedItem[0]))

      if (filters[key] && filters[key].length) {
        if (
          Array.isArray(filters[key]) &&
          filters[key].filter((node) => node === removedItem[0]).length
        ) {
          filters[key] = filters[key].filter((node) => node !== removedItem[0])
          // break
        } else if (filters[key] === removedItem[0]) {
          filters[key] = null
          // break
        }
      }
    }
    dispatch('setFilters', filters)
  },
  async getInfluencers({ state, commit }) {
    const client = this.app.apolloProvider.defaultClient
    try {
      const { data } = await client.query({
        query: gql`
          query SearchSeoInfluencers(
            $after: String
            $size: Int = 10
            $query: SearchQuery!
          ) {
            searchSeoInfluencers(after: $after, size: $size, query: $query) {
              edges {
                node {
                  title
                  country
                  slug
                  label
                  category
                  ccatid
                  language
                  type
                  categorySlug
                  countrySlug
                  labelSlug
                  instagram {
                    title
                    thumbnail
                    userid
                    username
                    description
                    category
                    statistics {
                      v30
                      er30
                      views
                      followers
                      uploads
                    }
                  }
                  youtube {
                    title
                    description
                    thumbnail
                    userid
                    category
                    cstatus
                    createdat
                    username
                    demographic
                    statistics {
                      v30
                      er30
                      views
                      followers
                      uploads
                      comments
                      views_7
                      followers_7
                      uploads_7
                      views_30
                      followers_30
                      uploads_30
                      views_90
                      followers_90
                      uploads_90
                    }
                  }
                }
              }
              pageInfo {
                hasNextPage
                hasPreviousPage
                total
                endCursor
                startCursor
              }
            }
          }
        `,
        variables: {
          query: {
            filters: state.formattedFilters,
            orderBy: state.sortingModal.selectedSort.value,
            orderDirection: state.sortingModal.selectedSort.order,
          },
          size: state.influencersModal.limit,
          after: state.influencersModal.endCursor,
        },
        context: {
          headers: {
            'x-bb-clientid': '8VX2KOK5GL3ctCqo1d0R',
          },
        },
      })
      if (data) commit('UPDATE_INFLUENCERS', data)
      return true
    } catch (error) {
      console.log(error)
    }
  },
  async getInfluencerDetails({ state, commit }) {
    const client = this.app.apolloProvider.defaultClient
    try {
      const { data } = await client.query({
        query: gql`
          query GetSeoInfluencer($id: ID!) {
            getSeoInfluencer(id: $id) {
              title
              country
              ccatid
              category
              label
              slug
              language
              type
              categorySlug
              countrySlug
              labelSlug
              instagram {
                title
                thumbnail
                userid
                username
                category
                description
                statistics {
                  v30
                  er30
                  views
                  followers
                  uploads
                }
              }
              youtube {
                title
                description
                thumbnail
                userid
                category
                cstatus
                createdat
                username
                demographic
                statistics {
                  v30
                  er30
                  views
                  followers
                  uploads
                  comments
                  views_7
                  followers_7
                  uploads_7
                  views_30
                  followers_30
                  uploads_30
                  views_90
                  followers_90
                  uploads_90
                }
              }
            }
          }
        `,
        variables: {
          id: state.influencerModal.slug,
        },
        context: {
          headers: {
            'x-bb-clientid': '8VX2KOK5GL3ctCqo1d0R',
          },
        },
      })
      if (data && data.getSeoInfluencer)
        commit('UPDATE_INFLUENCER_DETAILS', data.getSeoInfluencer)
    } catch (error) {
      commit('UPDATE_INFLUENCER_DETAILS', null)
      console.log(error)
    }
  },
  toggleFilter({ commit }) {
    commit('TOGGLE_FILTER')
  },
  setInfluencerSort({ commit, dispatch, state }, payload) {
    commit('UPDATE_SORTING', payload)
    dispatch('resetInfluencerList')
  },
  resetInfluencerList({ commit, dispatch, state }, payload) {
    commit('RESET_INFLUENCER_DATA', payload)
    dispatch('getInfluencers')
  },
  loadMorePage({ commit, dispatch, state }, payload) {
    if (!state.influencersModal.data[state.influencersModal.page]) {
      commit('UPDATE_MORE_PAGE', payload)
      dispatch('getInfluencers')
    }
  },
  changePage({ commit, dispatch }, payload) {
    document.body.scrollTop = document.documentElement.scrollTop = 0

    commit('UPDATE_PAGE_INDEX', payload)

    dispatch('loadMorePage', payload)
  },
  formatFilters({ commit }, payload) {
    const formattedFilters = []
    const filterData = {}
    if (payload && payload.length) {
      let filter = null

      if ((filter = payload.find((ob) => ob.field === 'categoryId'))) {
        formattedFilters.push({
          field: 'categoryId',
          value: filter.value,
          filterType: 'EQ',
        })
        filterData.categoryId = filter.value
      }

      if ((filter = payload.find((ob) => ob.field === 'platform'))) {
        formattedFilters.push({
          field: 'platform',
          value: filter.value,
          filterType: 'EQ',
        })
        filterData.platform = filter.value
      }
      if ((filter = payload.find((ob) => ob.field === 'max_followers'))) {
        formattedFilters.push({
          field: 'max_followers',
          value: filter.value,
          filterType: 'EQ',
        })
        filterData.max_followers = filter.value
      }
    }

    commit('UPDATE_FILTERS', filterData)
    commit('UPDATE_FORMATTED_FILTERS', formattedFilters)

    return true
  },
  toggleInfluencerDetails({ commit }, flag) {
    commit('TOGGLE_INFLUENCER_DETAILS', flag)
  },
  updateFiltersSlug({ commit }, payload) {
    commit('UPDATE_FILTERS_SLUG', payload)
  },
}

export const mutations = {
  UPDATE_LOGGEDIN(state, payload) {
    state.loggedIn = payload
  },
  UPDATE_USERINFO(state, payload) {
    state.userInfo = payload
  },
}

export const getters = {
  loggedIn: (state) => {
    return state.loggedIn
  },
  userInfo: (state) => {
    return state.userInfo
  },
}
