 <template>
  <div
    v-if="ticket"
    style="width: 100%; display: flex; flex-direction: column; gap: 30px"
  >
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
          margin: 20px 0 10px 0;
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
        <v-btn
          v-if="user && !user.admin && allowReply && !ticket.user_id"
          color="green"
          style="color: white"
          :disabled="ticket.status == 'Solved'"
          @click="markAsSolved"
          >Mark as solved</v-btn
        >
      </div>

      <div v-if="allowReply" style="margin-top: 20px">
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
  name: 'TicketDetails',
  mixins: [validationMixin],
  middleware: 'authenticated',
  validations: {
    newReply: { required },
  },
  props: {
    allowReply: {
      default: false,
      type: Boolean,
    },
  },
  data() {
    return {
      ticket: [],
      newReply: null,
    }
  },
  computed: {
    ...mapGetters({
      user: 'user/userInfo',
      selectedTicket: 'user/selectedTicket',
    }),
    newReplyErrors() {
      const errors = []
      if (!this.$v.newReply.$dirty) return errors

      !this.$v.newReply.required && errors.push('please enter a reply')
      return errors
    },
  },
  created() {
    this.getTicket()
  },
  methods: {
    ...mapActions({ switchTab: 'user/switchTab' }),
    async getTicket() {
      const { data } = await this.$repositories.ticket.getTicket({
        ticket_id: this.selectedTicket,
      })
      this.ticket = data
      // this.tickets = Object.values(data)
    },
    submit() {
      this.$v.$touch()
      if (!this.newReplyErrors.length) {
        this.replyHandler()
      }
    },
    async replyHandler() {
      const data = await this.$repositories.ticket.replyTicket({
        title: this.title,
        newReply: this.newReply,
        date: Date.now(),
      })
      if (data && data.data && data.data.success && data.status === 200) {
        this.ticket.replies.push([this.user.id, this.newReply])
      }
    },
    async markAsSolved() {
      const data = await this.$repositories.ticket.markAsSolved({
        ticket_id: this.ticket.id,
      })
      console.log(data)
      if (data && data.status === 201) {
        this.ticket.status = 'Solved'
      }
    },
  },
}
</script>