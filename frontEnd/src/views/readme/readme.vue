<template>
  <MdEditor v-model="text" />
</template>

<script setup>
import { ref } from 'vue';
import MdPreview from 'md-editor-v3';
import 'md-editor-v3/lib/style.css';
// import 'md-editor-v3/lib/preview.css';

const text = ref('Hello Editor!');
</script>