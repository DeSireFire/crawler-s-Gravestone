import { defineStore } from "pinia";
import { useStateStorage } from "~/utils/cache";

interface ObjectList {
  [key: string]: string[];
}

const { useJsonStorage } = useStateStorage();

export const usePermissStore = defineStore("permiss", {
  state: () => ({
    // 用户权限列表缓存到 localstorage 的 ms_keys 中
    key: useJsonStorage<string[]>("ms_keys", []),
    defaultList: <ObjectList>{
      admin: [
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "11",
        "12",
        "13",
        "14",
        "15",
        "16",
      ],
      user: ["1", "2", "3", "11", "13", "14", "15"],
    },
  }),
  actions: {
    handleSet(val: string[]) {
      this.key = val;
      // console.log(this.key, val)
    },
  },
});
