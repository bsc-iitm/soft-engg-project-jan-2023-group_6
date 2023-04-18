<template>
  <div>
    <div v-for="faq in faqs" :key="faq.id">
      <form v-if="faqUnderEdit && faqUnderEdit.id == faq.id" class="my-4">
        <v-text-field
          v-model="faqUnderEdit.title"
          label="title"
          required
          outlined
        >
        </v-text-field>
        <v-textarea
          v-model="faqUnderEdit.content"
          label="content"
          required
          outlined
        >
        </v-textarea>
        <v-btn @click="updateFaq">Update</v-btn>
      </form>
    
      <v-row v-else>
        <v-col>
          <v-expansion-panels>
            <v-expansion-panel>
              <v-expansion-panel-header>{{ faq.title }}</v-expansion-panel-header>
              <v-expansion-panel-content>{{ faq.content }}</v-expansion-panel-content>
            </v-expansion-panel>
          </v-expansion-panels>
        </v-col>
        <v-col cols="1">
          <v-btn @click="faqUnderEdit = faq">Edit</v-btn>
          <v-btn>Delete</v-btn>
        </v-col>
      </v-row>
    </div>
  </div>
</template>

<script>
export default {
  layout: 'empty',

  data() {
    return {
      faqs: null,
      faqUnderEdit: null
    }
  },

  created() {
    this.fetch_faqs()
  },

  methods: {
    async fetch_faqs() {
      const temp = await this.$repositories.faqs.get_faqs()
      this.faqs = temp.data.faqs
    },
    
    async updateFaq() {
      await this.$repositories.faqs.update_faq({
        id: this.faqUnderEdit.id,
        title: this.faqUnderEdit.title,
        content: this.faqUnderEdit.content
      })
      this.$router.push({
        path: '/faq',
      })
    }
  }
}
</script>