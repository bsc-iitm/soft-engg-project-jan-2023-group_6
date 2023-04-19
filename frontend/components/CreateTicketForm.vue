<template>
  <v-row align="center" justify="center" width="100%">
    <p v-show="createError" style="color: red; margin-top: 4%">
      Something went wrong
    </p>
    <form class="form-align">
      <v-text-field
        v-model="title"
        :error-messages="titleErros"
        label="title"
        style="width: 100%"
        required
        @input="$v.title.$touch()"
        @blur="$v.title.$touch()"
        outlined
      ></v-text-field>
      <v-textarea
        v-model="content"
        style="margin-bottom: 20px; width: 100%"
        :error-messages="contentErrors"
        label="details"
        required
        @input="$v.content.$touch()"
        @blur="$v.content.$touch()"
        outlined
      ></v-textarea>
      <v-btn class="mr-4" style="max-width: 200px" @click="submit">
        Create Ticket
      </v-btn>
    </form>
  </v-row>
</template>

<script>
import { validationMixin } from 'vuelidate'
import { required } from 'vuelidate/lib/validators'
import { mapActions } from 'vuex'

export default {
  mixins: [validationMixin],

  validations: {
    title: { required },
    content: { required },
  },

  data: () => ({
    title: '',
    content: '',
    createError: false,
  }),

  computed: {
    titleErros() {
      const errors = []
      if (!this.$v.title.$dirty) return errors

      !this.$v.title.required && errors.push('please enter a title')
      return errors
    },
    contentErrors() {
      const errors = []
      if (!this.$v.content.$dirty) return errors

      !this.$v.content.required &&
        errors.push('please enter details about your query')
      return errors
    },
  },

  methods: {
    ...mapActions({ switchTab: 'user/switchTab' }),
    submit() {
      this.createError = false
      this.$v.$touch()
      if (!this.titleErros.length && !this.contentErrors.length) {
        this.createTicketHandler()
      }
    },
    async createTicketHandler() {
      const data = await this.$repositories.ticket.createTicket({
        title: this.title,
        content: this.content,
        date: Date.now(),
      })
      if (data && data.data && data.data.success && data.status === 200) {
        this.switchTab('Home')
      } else {
        this.createError = true
      }
    },
  },
}
</script>

<style scoped>
.form-align {
  width: 100%;
  margin-top: 2%;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
</style>