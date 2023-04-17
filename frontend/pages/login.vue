<template>
  <v-row align="center" justify="center" width="100%">
    <form class="form-align">
      <v-text-field
        v-model="username"
        :error-messages="usernameErros"
        label="username"
        style="width: 100%"
        required
        @input="$v.username.$touch()"
        @blur="$v.username.$touch()"
        outlined
      ></v-text-field>
      <v-text-field
        style="margin-bottom: 20px; width: 100%"
        v-model="password"
        :error-messages="passwordErrors"
        label="password"
        required
        @input="$v.password.$touch()"
        @blur="$v.password.$touch()"
        outlined
      ></v-text-field>
      <v-btn class="mr-4" style="min-width: 110px" @click="submit">
        login
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
  layout: 'empty',

  validations: {
    username: { required },
    password: { required },
  },

  data: () => ({
    username: '',
    password: '',
  }),

  computed: {
    usernameErros() {
      const errors = []
      if (!this.$v.username.$dirty) return errors

      !this.$v.username.required && errors.push('please enter your username')
      return errors
    },
    passwordErrors() {
      const errors = []
      if (!this.$v.password.$dirty) return errors

      !this.$v.password.required && errors.push('please enter your password')
      return errors
    },
  },

  methods: {
    ...mapActions({ addUser: 'user/addUser' }),
    submit() {
      this.$v.$touch()
      if (!this.usernameErros.length && !this.passwordErrors.length) {
        this.handleLogin()
      }
    },
    async handleLogin() {
      const { data } = await this.$repositories.auth.login({
        username: this.username,
        password: this.password,
      })
      if (
        data &&
        data.access_token &&
        data.user_details &&
        data.user_details.id
      ) {
        this.$cookies.set(
          'user',
          { token: data.access_token, ...data.user_details },
          {
            maxAge: 25 * 24 * 60 * 60,
            path: '/',
            domain: null,
          }
        )
        this.addUser(data.user_details)
        this.$router.push({
          path: '/',
        })
      }
    },
  },
}
</script>

<style scoped>
.form-align {
  width: 100%;
  max-width: 400px;
  margin-top: 20%;
  display: flex;
  flex-direction: column;
  gap: 4px;
  align-items: center;
}
</style>