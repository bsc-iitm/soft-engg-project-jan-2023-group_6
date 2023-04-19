 <template>
  <div style="width: 100%; display: flex; flex-direction: column; gap: 30px">
    <v-btn color="blue" style="max-width: 100px" @click="selectTicket(null)"
      >Back
    </v-btn>

    <v-card v-if="ticket" outlined style="width: 100%; padding: 20px">
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
        <div>
          <!-- <v-btn v-if="user && user.admin" color="orange" style="color: white"
            >Mark as duplicate</v-btn
          > -->
          <v-btn
            :disabled="
              user.admin || (ticket.likes && ticket.likes.includes(user.id))
            "
            color="blue"
            style="color: white; margin: 0 10px"
            @click="likeTicket"
            >Like {{ ticket.likes && ticket.likes.length }}</v-btn
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
      </div>
      <div
        v-for="reply in ticket.replies"
        :key="reply[0] + 'b' + reply[1]"
        style="margin-top: 20px"
      >
        <v-card
          outlined
          style="
            width: 100%;
            padding: 4px;
            margin: 20px 0 10px 0;
            min-height: 130px;
          "
        >
          <v-card-title style="font-size: 14px">{{ reply[0] }}</v-card-title>
          <v-card-subtitle>{{ reply[1] }}</v-card-subtitle>
        </v-card>
      </div>
      <div v-if="allowReply" style="margin-top: 20px">
        <v-textarea
          v-model="newReply"
          style="margin-bottom: 0px; width: 100%"
          :error-messages="newReplyErrors"
          label="details"
          required
          outlined
          @input="$v.newReply.$touch()"
          @blur="$v.newReply.$touch()"
        ></v-textarea>
        <v-btn color="blue" style="color: white" @click="submit">Reply</v-btn>
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
    ...mapActions({
      switchTab: 'user/switchTab',
      selectTicket: 'user/selectTicket',
    }),
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
        ticket_id: this.selectedTicket,
        content: this.newReply,
      })
      if (data && data.status === 200) {
        this.ticket.replies.push([this.user.username, this.newReply])
      }
    },
    async markAsSolved() {
      const data = await this.$repositories.ticket.markAsSolved({
        ticket_id: this.ticket.id,
      })
      if (data && data.status === 201) {
        this.ticket.status = 'Solved'
      }
    },
    async likeTicket() {
      const data = await this.$repositories.ticket.likeTicket({
        ticket_id: this.ticket.id,
      })
      if (data && data.status === 201) {
        this.ticket.likes.push(this.user.id)
      }
    },
  },
}
</script>