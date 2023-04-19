 <template>
  <div style="width: 100%; display: flex; flex-direction: column; gap: 30px">
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

    <v-card outlined style="width: 100%; padding: 20px">
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
        <v-btn v-if="user && user.admin" color="orange" style="color: white"
          >Mark as duplicate</v-btn
        >
      </div>

      <div>
        <v-textarea
          v-model="newReply"
          style="margin-bottom: 20px; width: 100%"
          :error-messages="newReplyErrors"
          label="details"
          required
          outlined
          @input="$v.newReply.$touch()"
          @blur="$v.newReply.$touch()"
        ></v-textarea>
        <v-btn color="blue" style="color: white">Reply</v-btn>
      </div>
    </v-card>
  </div>
</template>

<script>
import { validationMixin } from 'vuelidate'
import { required } from 'vuelidate/lib/validators'
import { mapGetters, mapActions } from 'vuex'
export default {
  name: 'IndexPage',
  middleware: 'authenticated',
  mixins: [validationMixin],

  validations: {
    content: { required },
  },
  props: ['ticketID'],
  data() {
    return {
      ticketData: [],
      newReply: null,
    }
  },
  computed: {
    ...mapGetters({
      user: 'user/userInfo',
    }),
    newReplyErrors() {
      const errors = []
      if (!this.$v.newReply.$dirty) return errors

      !this.$v.newReply.required && errors.push('please enter a reply')
      return errors
    },
  },
  created() {
    this.getTickets()
  },
  methods: {
    ...mapActions({ switchTab: 'user/switchTab' }),
    async getTickets() {
      const { data } = await this.$repositories.ticket.getTickets()
      this.tickets = Object.values(data)
    },
    submit() {
      this.$v.$touch()
      if (!this.newReplyErrors.length) {
        this.createTicketHandler()
      }
    },
    async createTicketHandler() {
      const data = await this.$repositories.ticket.createTicket({
        title: this.title,
        newReply: this.newReply,
        date: Date.now(),
      })
      if (data && data.data && data.data.success && data.status === 200) {
        this.ticketData.replies.push([this.user.id, this.newReply])
      }
    },
  },
}
</script>