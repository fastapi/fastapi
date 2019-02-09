<template>
  <v-container fluid>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Edit User</div>
      </v-card-title>
      <v-card-text>
        <template>
          <div class="my-3">
            <div class="subheading secondary--text text--lighten-2">Username</div>
            <div class="title primary--text text--darken-2" v-if="user">{{user.name}}</div>
            <div class="title primary--text text--darken-2" v-else>-----</div>
          </div>
          <v-form v-model="valid" ref="form" lazy-validation>
            <v-text-field label="Full Name" v-model="fullName" required></v-text-field>
            <v-text-field label="E-mail" type="email" v-model="email" v-validate="'required|email'" data-vv-name="email" :error-messages="errors.collect('email')" required></v-text-field>
            <div class="subheading secondary--text text--lighten-2">Roles</div>
            <v-checkbox v-for="(value, role) in selectedRoles" :key="role" :label="role" v-model="selectedRoles[role]"></v-checkbox>
            <div class="subheading secondary--text text--lighten-2">Disable User <span v-if="userDisabled">(currently disabled)</span><span v-else>(currently enabled)</span></div>
            <v-checkbox :label="'Disabled'" v-model="userDisabled"></v-checkbox>
            <v-layout align-center>
              <v-flex shrink>
                <v-checkbox v-model="setPassword" class="mr-2"></v-checkbox>
              </v-flex>
              <v-flex>
                <v-text-field :disabled="!setPassword" type="password" ref="password" label="Set Password" data-vv-name="password" data-vv-delay="100" v-validate="{required: setPassword}" v-model="password1" :error-messages="errors.first('password')">
                </v-text-field>
                <v-text-field v-show="setPassword" type="password" label="Confirm Password" data-vv-name="password_confirmation" data-vv-delay="100" data-vv-as="password" v-validate="{required: setPassword, confirmed: 'password'}" v-model="password2" :error-messages="errors.first('password_confirmation')">
                </v-text-field>
              </v-flex>

            </v-layout>

            <v-btn @click="submit" :disabled="!valid">
              Save
            </v-btn>
            <v-btn @click="reset">Reset</v-btn>
            <v-btn @click="cancel">Cancel</v-btn>
          </v-form>
        </template>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { IUserProfile, IUserProfileUpdate } from '@/interfaces';
import {
  dispatchGetUsers,
  dispatchGetRoles,
  dispatchUpdateUser,
  readAdminOneUser,
  readAdminRoles,
} from '@/store/admin/accessors';

@Component
export default class EditUser extends Vue {
  public valid = true;
  public name: string = '';
  public fullName: string = '';
  public email: string = '';
  public setPassword = false;
  public password1: string = '';
  public password2: string = '';
  public userDisabled: boolean = false;

  public selectedRoles: { [role: string]: boolean } = {};

  public async mounted() {
    await dispatchGetUsers(this.$store);
    await dispatchGetRoles(this.$store);
    this.availableRoles.forEach((value) => {
      Vue.set(this.selectedRoles, value, false);
    });
    this.reset();
  }

  public reset() {
    this.setPassword = false;
    this.password1 = '';
    this.password2 = '';
    this.$validator.reset();
    if (this.user) {
      this.name = this.user.name;
      this.fullName = this.user.human_name;
      this.email = this.user.email;
      this.userDisabled = this.user.disabled;
      this.availableRoles.forEach((role: string) => {
        if (this.user!.admin_roles.includes(role)) {
          Vue.set(this.selectedRoles, role, true);
        } else {
          Vue.set(this.selectedRoles, role, false);
        }
      });
    }
  }

  public cancel() {
    this.$router.back();
  }

  public async submit() {
    if (await this.$validator.validateAll()) {
      const updatedProfile: IUserProfileUpdate = {};
      if (this.fullName) {
        updatedProfile.human_name = this.fullName;
      }
      if (this.email) {
        updatedProfile.email = this.email;
      }
      updatedProfile.disabled = this.userDisabled;
      updatedProfile.admin_roles = [];
      this.availableRoles.forEach((role: string) => {
        if (this.selectedRoles[role]) {
          updatedProfile.admin_roles!.push(role);
        }
      });
      if (this.setPassword) {
        updatedProfile.password = this.password1;
      }
      const payload = { name: this.name, user: updatedProfile };
      await dispatchUpdateUser(this.$store, payload);
      this.$router.push('/main/admin/users');
    }
  }

  get user() {
    return readAdminOneUser(this.$store)(this.$router.currentRoute.params.name);
  }

  get availableRoles() {
    return readAdminRoles(this.$store);
  }
}
</script>
