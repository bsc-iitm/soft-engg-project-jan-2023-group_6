<template>
  <v-row style="gap: 30px; margin-bottom: 14px">
    <h1>{{ user && user.admin ? 'Open Tickets' : 'Your Tickets' }}</h1>
    <v-card
      outlined
      style="width: 100%; padding: 20px"
      v-for="ticket in tickets"
      :key="ticket.id"
    >
      <div style="display: flex; gap: 40px">
        <span>Ticket #{{ ticket.id }}</span>
        <span style="margin-left: 40px" v-if="ticket.tags"
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
        <v-btn color="blue" style="color: white">View Details</v-btn>
      </div>
    </v-card>
  </v-row>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  name: 'IndexPage',
  middleware: 'authenticated',

  data() {
    return {
      tickets: [],
      ticket: {
        id: 234,
        tags: ['Course', 'Misc'],
        title: 'New course',
        content:
          'ADKJ KJFLKJS KLJFLSDKJF LKSJFL KSJFLKJ SLKFJLKSD JFKLSDJFLKSDFJL ADKJ KJFLKJS KLJFLSDKJF LKSJFL KSJFLKJ SLKFJLKSD JFKLSDJFLKSDFJLADKJ KJFLKJS KLJFLSDKJF LKSJFL KSJFLKJ SLKFJLKSD JFKLSDJFLKSDFJLADKJ KJFLKJS KLJFLSDKJF LKSJFL KSJFLKJ SLKFJLKSD JFKLSDJFLKSDFJLADKJ KJFLKJS KLJFLSDKJF LKSJFL KSJFLKJ SLKFJLKSD JFKLSDJFLKSDFJLADKJ KJFLKJS KLJFLSDKJF LKSJFL KSJFLKJ SLKFJLKSD JFKLSDJFLKSDFJLADKJ KJFLKJS KLJFLSDKJF LKSJFL KSJFLKJ SLKFJLKSD JFKLSDJFLKSDFJLADKJ KJFLKJS KLJFLSDKJF LKSJFL KSJFLKJ SLKFJLKSD JFKLSDJFLKSDFJLADKJ KJFLKJS KLJFLSDKJF LKSJFL KSJFLKJ SLKFJLKSD JFKLSDJFLKSDFJLADKJ KJFLKJS KLJFLSDKJF LKSJFL KSJFLKJ SLKFJLKSD JFKLSDJFLKSDFJLADKJ KJFLKJS KLJFLSDKJF LKSJFL KSJFLKJ SLKFJLKSD JFKLSDJFLKSDFJLADKJ KJFLKJS KLJFLSDKJF LKSJFL KSJFLKJ SLKFJLKSD JFKLSDJFLKSDFJLADKJ KJFLKJS KLJFLSDKJF LKSJFL KSJFLKJ SLKFJLKSD JFKLSDJFLKSDFJL',
        status: 'Resolved',
      },
    }
  },
  computed: {
    ...mapGetters({
      user: 'user/userInfo',
    }),
  },
  created() {
    this.getTickets()
  },
  methods: {
    async getTickets() {
      const { data } = await this.$repositories.ticket.getTickets()
      console.log(data)
      this.tickets = Object.values(data)
    },
  },
}
</script>
