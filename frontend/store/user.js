export const state = () => ({
  loggedIn: false,
  userInfo: {},
  currentTab: 'Home',
})

export const actions = {
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

  addUser({ commit }, payload) {
    commit('UPDATE_LOGGEDIN', true)
    commit('UPDATE_USERINFO', payload)
  },
  clearUser({ commit }) {
    commit('UPDATE_LOGGEDIN', false)
    commit('UPDATE_USERINFO', {})
  },
  switchTab({ commit }, payload) {
    commit('UPDATE_TAB', payload)
  },
}

export const mutations = {
  UPDATE_LOGGEDIN(state, payload) {
    state.loggedIn = payload
  },
  UPDATE_USERINFO(state, payload) {
    state.userInfo = payload
  },
  UPDATE_TAB(state, payload) {
    state.currentTab = payload
  },
}

export const getters = {
  loggedIn: (state) => {
    return state.loggedIn
  },
  userInfo: (state) => {
    return state.userInfo
  },
  currentTab: (state) => {
    return state.currentTab
  },
}
