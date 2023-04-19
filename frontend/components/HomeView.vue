 <template>
  <div
    v-if="!this.selectedTicket"
    style="width: 100%; display: flex; flex-direction: column; gap: 30px"
  >
    <div
      style="
        display: flex;
        justify-content: space-between;
        width: 100%;
        margin-bottom: -20px;
      "
    >
      <h1>{{ user && user.admin ? 'Open Tickets' : 'Your Tickets' }}</h1>
      <v-btn
        v-if="user && !user.admin"
        color="red"
        style="color: white"
        @click="switchTab('CreateTicket')"
        >Raise ticket</v-btn
      >
    </div>

    <v-card
      v-for="ticket in tickets"
      :key="ticket.id"
      outlined
      style="width: 100%; padding: 20px"
    >
      <div style="display: flex; gap: 40px">
        <span>Ticket #{{ ticket.id }}</span>
        <span v-if="ticket.tags" style="margin-left: 40px"
          >Tags: {{ ticket.tags.join(', ') }}</span
        >
      </div>
      <v-card
        outlined
        style="
          width: 100%;
          padding: 4px;
          margin: 20px 0 30px 0;
          min-height: 130px;
          max-height: 130px;
          overflow: hidden;
        "
      >
        <v-card-title>{{ ticket.title }}</v-card-title>
        <v-card-subtitle>{{ ticket.content }}</v-card-subtitle>
      </v-card>

      <div
        style="
          display: flex;
          gap: 40px;
          align-items: center;
          justify-content: space-between;
        "
      >
        <span
          >Status:
          <span
            :style="{
              color: ticket.status == 'Open' ? 'red' : 'green',
              fontWeight: 700,
            }"
          >
            {{ ticket.status }}
          </span></span
        >
        <v-btn
          color="blue"
          style="color: white"
          @click="selectTicket(ticket.id)"
          >View Details</v-btn
        >
      </div>
    </v-card>
  </div>
  <ticket-details :allowReply="true" v-else> </ticket-details>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import TicketDetails from './TicketDetails.vue'
export default {
  components: { TicketDetails },
  name: 'IndexPage',
  middleware: 'authenticated',

  data() {
    return {
      tickets: [],
      retryCounts: 1,
    }
  },
  computed: {
    ...mapGetters({
      user: 'user/userInfo',
      selectedTicket: 'user/selectedTicket',
    }),
  },
  created() {
    this.getTickets()
  },
  methods: {
    ...mapActions({
      switchTab: 'user/switchTab',
      selectTicket: 'user/selectTicket',
    }),
    async getTickets() {
      try {
        const data = await this.$repositories.ticket.getTickets()
        console.log(data)
        this.tickets = Object.values(data.data)
      } catch {
        if (this.retryCounts < 5) {
          window.location.reload()
        }
      }
    },
  },
}
</script>