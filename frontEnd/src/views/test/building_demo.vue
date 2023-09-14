<template>
  <div class="container">
    <div class="plugins-tips">
      <b>页面施工中</b>
    </div>
    <MdPreview :editorId="mdTId" :modelValue="text" />
  </div>
</template>

<script setup lang="ts" name="md">
import { ref, onMounted,watch } from 'vue';
import { MdPreview,MdEditor, MdCatalog } from 'md-editor-v3';
import 'md-editor-v3/lib/preview.css';
const mdTId = 'md_text';
const text = ref('**页面施工中**....!');
</script>
