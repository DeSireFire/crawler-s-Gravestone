import { MaybeRef, UseStorageOptions, useLocalStorage } from "@vueuse/core";

/**
 * 自动在 localStorage 和 store 之间同步数据
 */

const useStateSerializer = () => ({
  write(val: unknown) {
    return JSON.stringify(val);
  },
  read(raw: string) {
    return JSON.parse(raw);
  },
});

const useSimpleStorage = useLocalStorage;
const useJsonStorage = <T = unknown>(
  key: string,
  initialValue: MaybeRef<T>,
  options?: UseStorageOptions<T>
) => {
  const serializer = useStateSerializer();
  return useSimpleStorage<T>(key, initialValue, { ...options, serializer });
};

export const useStateStorage = () => ({
  // 缓存 基本 数据
  useSimpleStorage,
  // 缓存 对象 数据
  useJsonStorage,
});
