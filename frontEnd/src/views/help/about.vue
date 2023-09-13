<template>
  <div class="container">
    <div class="plugins-tips">
      <b>关于 - 数据矿工管理平台</b>
    </div>
    <div>
      <MdPreview :editorId="mdTId" :modelValue="mdText" />
    </div>
    <el-scrollbar class="preview">
      <MdPreview :editorId="mdId" :modelValue="mdAbout" />
    </el-scrollbar>
  </div>
</template>

<script setup lang="ts" name="about">
import { ref, onMounted,watch } from 'vue';
import { MdPreview,MdEditor, MdCatalog } from 'md-editor-v3';
import 'md-editor-v3/lib/preview.css';
import 关于 from '~/assets/md/关于.md?raw'; // 根据实际路径调整

const mdId = 'md_about';
const mdAbout = ref('');
const mdTId = 'md_text';
const mdText = ref('# 数据矿工管理平台 版本: 【Version 1.6】');

// 加载 markdown 文本文件内容
const loadMarkdownContent = async () => {
  mdAbout.value = 关于;
};

// 在组件挂载后加载并渲染 Markdown 内容
// 在组件挂载后加载文本文件内容，并在文本文件发生更改时重新加载
onMounted(() => {
  loadMarkdownContent();
});
</script>

<style scoped>
.preview {
  height: 500px;
}
</style>
