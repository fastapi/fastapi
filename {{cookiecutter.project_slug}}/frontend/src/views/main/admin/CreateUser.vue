<template>
  <v-container fluid>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Create User</div>
      </v-card-title>
      <v-card-text>
        <template>
          <v-form v-model="valid" ref="form" lazy-validation>
            <v-text-field label="Username" v-model="name" required></v-text-field>
            <v-text-field label="Full Name" v-model="fullName" required></v-text-field>
            <v-text-field label="E-mail" type="email" v-model="email" v-validate="'required|email'" data-vv-name="email" :error-messages="errors.collect('email')" required></v-text-field>
            <div class="subheading secondary--text text--lighten-2">Roles</div>
            <v-checkbox v-for="(value, role) in selectedRoles" :key="role" :label="role" v-model="selectedRoles[role]"></v-checkbox>
            <div class="subheading secondary--text text--lighten-2">Disable User <span v-if="userDisabled">(currently disabled)</span><span v-else>(currently enabled)</span></div>
            <v-checkbox :label="'Disabled'" v-model="userDisabled"></v-checkbox>
            <v-layout align-center>
              <v-flex>
                <v-text-field type="password" ref="password" label="Set Password" data-vv-name="password" data-vv-delay="100" v-validate="{required: true}" v-model="password1" :error-messages="errors.first('password')">
                </v-text-field>
                <v-text-field type="password" label="Confirm Password" data-vv-name="password_confirmation" data-vv-delay="100" data-vv-as="password" v-validate="{required: true, confirmed: 'password'}" v-model="password2" :error-messages="errors.first('password_confirmation')">
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
import {
  IUserProfile,
  IUserProfileUpdate,
  IUserProfileCreate,
} from '@/interfaces';
import { dispatchGetUsers, dispatchGetRoles, dispatchCreateUser, readAdminRoles } from '@/store/admin/accessors';

@Component
export default class EditUser extends Vue {
  public valid = false;
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
    this.reset();
  }

  public reset() {
    this.password1 = '';
    this.password2 = '';
    this.name = '';
    this.fullName = '';
    this.email = '';
    this.userDisabled = false;
    this.$validator.reset();
    this.availableRoles.forEach((value) => {
      Vue.set(this.selectedRoles, value, false);
    });
  }

  public cancel() {
    this.$router.back();
  }

  public async submit() {
    if (await this.$validator.validateAll()) {
      const updatedProfile: IUserProfileCreate = {
        name: this.name,
      };
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
      updatedProfile.password = this.password1;
      await dispatchCreateUser(this.$store, updatedProfile);
      this.$router.push('/main/admin/users');
    }
  }

  get availableRoles() {
    return readAdminRoles(this.$store);
  }
}
</script>
