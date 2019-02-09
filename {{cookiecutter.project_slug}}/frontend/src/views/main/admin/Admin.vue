<template>
    <router-view></router-view>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { store } from '@/store';
import { readHasAdminAccess } from '@/store/main/accessors';
import { dispatchGetRoles } from '@/store/admin/accessors';

const routeGuardAdmin = async (to, from, next) => {
  if (!readHasAdminAccess(store)) {
    next('/main');
  } else {
    next();
  }
};

@Component
export default class Start extends Vue {
  public beforeRouteEnter(to, from, next) {
    routeGuardAdmin(to, from, next);
  }

  public beforeRouteUpdate(to, from, next) {
    routeGuardAdmin(to, from, next);
  }

  public async mounted() {
    await dispatchGetRoles(this.$store);
  }
}
</script>
