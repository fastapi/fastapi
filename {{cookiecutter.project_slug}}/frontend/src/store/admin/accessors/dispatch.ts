import { getStoreAccessors } from 'typesafe-vuex';
import { AdminState } from '../state';
import { State } from '@/store/state';
import { actions } from '../actions';

const {dispatch} = getStoreAccessors<AdminState, State>('');

export const dispatchCreateUser = dispatch(actions.actionCreateUser);
export const dispatchGetRoles = dispatch(actions.actionGetRoles);
export const dispatchGetUsers = dispatch(actions.actionGetUsers);
export const dispatchUpdateUser = dispatch(actions.actionUpdateUser);
