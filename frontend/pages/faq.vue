<template>
  <v-expansion-panels>
    <v-expansion-panel v-for="faq in faqs" :key="faq.id">
      <v-expansion-panel-header>{{ faq.title }}</v-expansion-panel-header>
      <v-expansion-panel-content>{{ faq.content }}</v-expansion-panel-content>
    </v-expansion-panel>
  </v-expansion-panels>
</template>

<script>
export default {
  layout: 'empty',
  fetchOnServer: 'false',

  data: () => ({
    faqs: null
  }),

  async fetch() {
    const temp = await this.$repositories.faqs.get_faqs()
    this.faqs = temp.data.faqs
  }


}
</script>