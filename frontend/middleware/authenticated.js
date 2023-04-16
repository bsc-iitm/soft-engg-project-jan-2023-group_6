export default function ({ store, redirect }) {
  // If the user is not authenticated
  if (!store.state.user.loggedIn) {
    console.log(store)
    return redirect('/login')
  }
}
