<template>
  <v-row align="center" justify="center" width="100%">
    <form class="form-align">
      <v-row>
        <v-col>
          <v-text-field
            v-model="name"
            :error-messages="nameErrors"
            :counter="10"
            label="Name"
            required
            @input="$v.name.$touch()"
            @blur="$v.name.$touch()"
          ></v-text-field>
        </v-col>
        <v-col>
          <v-text-field
            v-model="username"
            :error-messages="usernameErrors"
            :counter="16"
            label="Username"
            required
            @input="$v.username.$touch()"
            @blur="$v.username.$touch()"
          ></v-text-field>
        </v-col>
      </v-row>
      <v-text-field
        v-model="email"
        :error-messages="emailErrors"
        label="E-mail"
        style="width: 100%"
        required
        @input="$v.email.$touch()"
        @blur="$v.email.$touch()"
      ></v-text-field>
      <v-text-field
        v-model="password"
        :error-messages="passwordErrors"
        label="Password"
        style="width: 100%"
        required
        @input="$v.password.$touch()"
        @blur="$v.password.$touch()"
      ></v-text-field>
      <v-checkbox
        v-model="checkbox"
        :error-messages="checkboxErrors"
        label="Do you agree?"
        required
        @change="$v.checkbox.$touch()"
        @blur="$v.checkbox.$touch()"
      ></v-checkbox>
      <v-btn class="mr-4" @click="submit">Submit</v-btn>
      <span class="mt-2">Already have an account? <a href="/login" style="text-decoration: none;">Login instead</a></span>
    </form>
  </v-row>
</template>

<script>
import { validationMixin } from 'vuelidate'
import { required, maxLength, email } from 'vuelidate/lib/validators'

export default {
  mixins: [validationMixin],
  layout: 'empty',

  validations: {
    name: { required, maxLength: maxLength(10) },
    username: { required, maxLength: maxLength(16) },
    email: { required, email },
    password: { required },
    checkbox: {
      checked(val) {
        return val
      },
    },
  },

  data: () => ({
    name: '',
    email: '',
    username: '',
    password: '',
    checkbox: false,
  }),

  computed: {
    checkboxErrors() {
      const errors = []
      if (!this.$v.checkbox.$dirty) return errors
      !this.$v.checkbox.checked && errors.push('You must agree to continue!')
      return errors
    },
    nameErrors() {
      const errors = []
      if (!this.$v.name.$dirty) return errors
      !this.$v.name.maxLength &&
        errors.push('Name must be at most 10 characters long')
      !this.$v.name.required && errors.push('Name is required.')
      return errors
    },
    emailErrors() {
      const errors = []
      if (!this.$v.email.$dirty) return errors
      !this.$v.email.email && errors.push('Must be valid e-mail')
      !this.$v.email.required && errors.push('E-mail is required')
      return errors
    },
    usernameErrors() {
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
    submit() {
      this.$v.$touch()
      if (!this.checkboxErrors.length && !this.nameErrors.length && !this.emailErrors.length && !this.usernameErrors.length && !this.passwordErrors.length) {
        this.handleSignUp()
      }
    },
    async handleSignUp() {
      const { data } = await this.$repositories.auth.signup({
        name: this.name,
        username: this.username,
        email: this.email,
        password: this.password,
        admin: 0
      })
      if (data.success) {
        this.$router.push({
          path: '/',
        })
      }
    },
    clear() {
      this.$v.$reset()
      this.name = ''
      this.email = ''
      this.select = null
      this.checkbox = false
    },
  },
}
</script>

<style scoped>
.form-align {
  width: 100%;
  max-width: 400px;
  margin-top: 15%;
  display: flex;
  flex-direction: column;
  gap: 4px;
  align-items: center;
}
</style>