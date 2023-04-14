import AuthRepository from '~/repositories/authRepository'
import FaqRepository from '~/repositories/faqRepository'

export default ($axios) => ({
  auth: AuthRepository($axios),
  faqs: FaqRepository($axios),
})
