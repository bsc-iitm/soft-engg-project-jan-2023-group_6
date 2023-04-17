import AuthRepository from '~/repositories/authRepository'
import TicketRepository from '~/repositories/ticketRepository'

export default ($axios) => ({
  auth: AuthRepository($axios),
  ticket: TicketRepository($axios),
})
