import path from "path";

import vue from "@vitejs/plugin-vue";
import AutoImport from "unplugin-auto-import/vite";
import { ElementPlusResolver } from "unplugin-vue-components/resolvers";
import Components from "unplugin-vue-components/vite";
import { defineConfig } from "vite";
import VueSetupExtend from "vite-plugin-vue-setup-extend";
export default defineConfig({
  base: "./",
  server: {
    host: '0.0.0.0',
    port: 50831,
    // 是否开启 https
    https: false,
  },
  plugins: [
    vue(),
    VueSetupExtend(),
    AutoImport({
      resolvers: [ElementPlusResolver()],
    }),
    Components({
      resolvers: [ElementPlusResolver()],
    }),
  ],
  optimizeDeps: {
    include: ["schart.js"],
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
      "~": path.resolve(__dirname, "./src"),
      "@@": path.resolve(__dirname, "./src"),
      "~~": path.resolve(__dirname, "./src"),
      "~/*": path.resolve(__dirname, "./src/*"),
      "@/*": path.resolve(__dirname, "./src/*"),
      "~~/*": path.resolve(__dirname, "./src/*"),
      "@@/*": path.resolve(__dirname, "./src/*"),
    },
  },
});
