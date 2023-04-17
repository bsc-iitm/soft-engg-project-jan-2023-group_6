export default function ({ store, redirect, commit, cookies }) {
  // If the user is not authenticated
  const user = store.$cookies.get('user')
  if (user && user.id && user.token) {
    store.dispatch('user/addUser', user)
  }
  if (!store.state.user.loggedIn) {
    return redirect('/login')
  }
}
