<template>
  <v-container>
    <div v-for="faq in faqs" :key="faq.id">
      <form v-if="faqUnderEdit && faqUnderEdit.id == faq.id">
        <v-text-field v-model="faqUnderEdit.title">
        </v-text-field>
        <v-text-field v-model="faqUnderEdit.content">
        </v-text-field>
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
  </v-container>
</template>

<script>
export default {
  layout: 'empty',
  fetchOnServer: 'false',

  data: () => ({
    faqs: null,
    faqUnderEdit: null
  }),

  async fetch() {
    const temp = await this.$repositories.faqs.get_faqs()
    this.faqs = temp.data.faqs
  },

  methods: {
    async updateFaq() {
      await this.$repositories.faqs.update_faq({
        title: this.faqUnderEdit.title,
        content: this.faqUnderEdit.content
      })
      document.location.reload()
    }
  }
}
</script>