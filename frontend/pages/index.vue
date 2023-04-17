<template>
  <v-row style="gap: 30px; margin-bottom: 14px">
    <home-view v-if="currentTab == 'Home'" />
    <create-ticket-form v-if="currentTab == 'CreateTicket'" />
  </v-row>
</template>

<script>
import { mapGetters } from 'vuex'
import CreateTicketForm from '../components/CreateTicketForm.vue'
import HomeView from '../components/HomeView.vue'
export default {
  components: { HomeView, CreateTicketForm },
  name: 'IndexPage',
  middleware: 'authenticated',

  computed: {
    ...mapGetters({
      user: 'user/userInfo',
      currentTab: 'user/currentTab',
    }),
  },
}
</script>
