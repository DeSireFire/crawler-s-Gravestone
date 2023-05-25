import { defineStore } from "pinia";
import { CacheKey } from "../constants/cache";
import { AccountModel } from "../models/account";
import { useStateStorage } from "../utils/cache";

const { useSimpleStorage, useJsonStorage } = useStateStorage();

export const useAccountStore = defineStore("accountStore", {
  state: () => ({
    authToken: useSimpleStorage<string | null>(CacheKey.AUTH_TOKEN, null),
    profile: useJsonStorage<AccountModel | null>(CacheKey.ACCOUNT, null),
  }),
  getters: {
    isLoggedIn: (state) => !!state.authToken,
  },
  actions: {
    setAuthToken(token: string | null) {
      this.authToken = token;
    },
    setProfile(profile: AccountModel | null) {
      this.profile = profile;
    },
  },
});
