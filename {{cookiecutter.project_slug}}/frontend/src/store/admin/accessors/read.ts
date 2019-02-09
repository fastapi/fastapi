import { getStoreAccessors } from 'typesafe-vuex';
import { AdminState } from '../state';
import { State } from '@/store/state';
import { getters } from '../getters';

const { read } = getStoreAccessors<AdminState, State>('');

export const readAdminOneUser = read(getters.adminOneUser);
export const readAdminRoles = read(getters.adminRoles);
export const readAdminUsers = read(getters.adminUsers);
