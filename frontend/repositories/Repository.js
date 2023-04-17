import AuthRepository from '~/repositories/authRepository'
import TicketRepository from '~/repositories/ticketRepository'
import FaqRepository from '~/repositories/faqRepository'

export default ($axios) => ({
  auth: AuthRepository($axios),
  ticket: TicketRepository($axios),
  faq: FaqRepository($axios),
})
