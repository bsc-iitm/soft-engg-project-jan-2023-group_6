import AuthRepository from '~/repositories/authRepository'

export default ($axios) => ({
  auth: AuthRepository($axios),
})
