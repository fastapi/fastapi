<template>
  <v-content>
    <v-container fluid fill-height>
      <v-layout align-center justify-center>
        <v-flex xs12 sm8 md4>
          <v-card class="elevation-12">
            <v-toolbar dark color="primary">
              <v-toolbar-title>{{appName}} - Reset Password</v-toolbar-title>
            </v-toolbar>
            <v-card-text>
              <p class="subheading">Enter your new password below</p>
              <v-form @keyup.enter="submit" v-model="valid" ref="form" @submit.prevent="" lazy-validation>
                <v-text-field type="password" ref="password" label="Password" data-vv-name="password" data-vv-delay="100" data-vv-rules="required" v-validate="'required'" v-model="password1" :error-messages="errors.first('password')">
                </v-text-field>
                <v-text-field type="password" label="Confirm Password" data-vv-name="password_confirmation" data-vv-delay="100" data-vv-rules="required|confirmed:$password" data-vv-as="password" v-validate="'required|confirmed:password'" v-model="password2" :error-messages="errors.first('password_confirmation')">
                </v-text-field>
              </v-form>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn @click="cancel">Cancel</v-btn>
              <v-btn @click="reset">Clear</v-btn>
              <v-btn @click="submit" :disabled="!valid">Save</v-btn>
            </v-card-actions>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </v-content>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { Store } from 'vuex';
import { IUserProfileUpdate } from '@/interfaces';
import { appName } from '@/env';
import { commitAddNotification } from '@/store/main/mutations';
import { dispatchResetPassword } from '@/store/main/actions';

@Component
export default class UserProfileEdit extends Vue {
  public appName = appName;
  public valid = true;
  public password1 = '';
  public password2 = '';

  public mounted() {
    this.checkToken();
  }

  public reset() {
    this.password1 = '';
    this.password2 = '';
    this.$validator.reset();
  }

  public cancel() {
    this.$router.push('/');
  }

  public checkToken() {
    const token = (this.$router.currentRoute.query.token as string);
    if (!token) {
      commitAddNotification(this.$store, {
        content: 'No token provided in the URL, start a new password recovery',
        color: 'error',
      });
      this.$router.push('/recover-password');
    } else {
      return token;
    }
  }

  public async submit() {
    if (await this.$validator.validateAll()) {
      const token = this.checkToken();
      if (token) {
        await dispatchResetPassword(this.$store, { token, password: this.password1 });
        this.$router.push('/');
      }
    }
  }
}
</script>
