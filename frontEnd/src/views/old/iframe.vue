<template>
  <div class="frame">
    <iframe :src="embeddedUrl" width="100%" height="780px"></iframe>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const embeddedUrl = ref('https://blog.raxianch.moe/');
</script>

<style scoped>
.frame {
  border: 1px solid #ddd;
  border-radius: 5px;
}
</style>
