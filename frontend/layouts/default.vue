<template>
  <v-app>
    <v-app-bar app>
      <v-app-bar-nav-icon
        @click="drawer = true"
        class="d-flex d-sm-none"
      ></v-app-bar-nav-icon>

      <v-tabs v-model="tab" align-with-title class="d-none d-sm-flex">
        <v-tabs-slider color="blue"></v-tabs-slider>

        <v-tab v-for="item in items" :key="item">
          {{ item }}
        </v-tab>
      </v-tabs>
      <v-btn color="blue" style="color: white">Logout</v-btn>
      <v-spacer></v-spacer>
    </v-app-bar>
    <!-- Add a navigation bar -->
    <v-navigation-drawer v-model="drawer" absolute temporary>
      <v-list nav dense>
        <v-list-item-group>
          <v-list-item v-for="(item, index) in items" :key="item">
            <v-list-item-title @click="tab = index">{{
              item
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

    <v-footer :absolute="!fixed" app>
      <span>Utopian Pind &copy; {{ new Date().getFullYear() }}</span>
    </v-footer>
  </v-app>
</template>

<script>
export default {
  name: 'DefaultLayout',
  data() {
    return {
      drawer: false,
      tab: null,
      items: ['web', 'shopping', 'videos', 'images', 'news'],
    }
  },
}
</script>
