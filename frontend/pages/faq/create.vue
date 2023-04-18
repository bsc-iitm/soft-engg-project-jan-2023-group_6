<template>
  <div>
    <h1 class="text-center">
      Create Faq
    </h1>
    <form class="mt-4">
      <v-text-field
        v-model="title"
        label="title"
        required
        outlined
      >
      </v-text-field>
      <v-textarea
        v-model="content"
        label="content"
        required
        outlined
      >
      </v-textarea>
      <v-btn @click="createFaq">Submit</v-btn>
    </form>
  </div>
</template>

<script>
export default {
  layout: 'empty',

  data() {
    return {
      title: null,
      content: null
    }
  },

  methods: {
    async createFaq() {
      await this.$repositories.faqs.create_faq({
        title: this.title,
        content: this.content
      })
      this.$router.push({
        path: '/faq',
      })
    }
  }


}
</script>