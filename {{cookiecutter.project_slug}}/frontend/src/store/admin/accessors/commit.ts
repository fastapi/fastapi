import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '@/store/state';
import { mutations } from '../mutations';
import { AdminState } from '../state';

const {commit} = getStoreAccessors<AdminState, State>('');

export const commitSetRoles = commit(mutations.setRoles);
export const commitSetUser = commit(mutations.setUser);
export const commitSetUsers = commit(mutations.setUsers);
