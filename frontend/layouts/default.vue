<template>
  <v-app>
    <v-app-bar app>
      <v-app-bar-nav-icon
        @click="drawer = true"
        class="d-flex d-sm-none"
      ></v-app-bar-nav-icon>

      <v-tabs v-model="tab" align-with-title class="d-none d-sm-flex">
        <v-tabs-slider color="blue"></v-tabs-slider>

        <v-tab v-for="item in pages" :key="item.title">
          <span @click="switchTab(item.title)">
            {{ item.title }}
          </span>
        </v-tab>
      </v-tabs>
      <v-btn color="blue" style="color: white" @click="logout">Logout</v-btn>
      <v-spacer></v-spacer>
    </v-app-bar>
    <!-- Add a navigation bar -->
    <v-navigation-drawer v-model="drawer" absolute temporary>
      <v-list nav dense>
        <v-list-item-group>
          <v-list-item v-for="item in pages" :key="item.title">
            <v-list-item-title @click="switchTab(item.title)">{{
              item.title
            }}</v-list-item-title>
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-navigation-drawer>
    <v-main style="margin-top: 20px">
      <v-container>
        <Nuxt />
      </v-container>
    </v-main>

    <v-footer app>
      <span>Utopian Pind &copy; {{ new Date().getFullYear() }}</span>
    </v-footer>
  </v-app>
</template>

<script>
import { mapActions } from 'vuex'
export default {
  name: 'DefaultLayout',
  data() {
    return {
      drawer: false,
      tab: null,
      pages: [
        { title: 'Home', route: '/' },
        { title: 'Posts', route: '/posts' },
        { title: 'FAQs', route: '/faq' },
      ],
    }
  },
  methods: {
    ...mapActions({ clearUser: 'user/clearUser', switchTab: 'user/switchTab' }),
    logout() {
      this.clearUser()
      this.$cookies.remove('user', { path: null, domain: null })
      this.$cookies.remove('user', { path: null, domain: '.' })
      this.$router.push('/login')
    },
  },
}
</script>
