<template>
  <div class="container">
    <div class="plugins-tips">
      <b>使用文档</b>
    </div>
    <div>
      <el-collapse v-model="activeName" accordion>
        <el-collapse-item name="1">
          <template #title>
            <b>如何获取工作流密钥？</b>
          </template>
          <el-scrollbar class="preview">
            <MdPreview :editorId="mdId1" :modelValue="markdownContent1" />
          </el-scrollbar>
        </el-collapse-item>
        <el-collapse-item name="2">
          <template #title>
            <b>监控信息推流客户端</b>
          </template>
          <el-scrollbar class="preview">
            <MdPreview :editorId="mdId2" :modelValue="markdownContent2" />
          </el-scrollbar>
        </el-collapse-item>
        <el-collapse-item name="3">
          <template #title>
            <b>告警管理的使用指南</b>
          </template>
          <el-scrollbar class="preview">
            <MdPreview :editorId="mdId3" :modelValue="markdownContent3" />
          </el-scrollbar>
        </el-collapse-item>
      </el-collapse>
    </div>
  </div>
</template>

<script setup lang="ts" name="md">
import { ref, onMounted,watch } from 'vue';
import { MdPreview,MdEditor, MdCatalog } from 'md-editor-v3';
import 'md-editor-v3/lib/preview.css';
import 如何获取工作流密钥 from '~/assets/md/如何获取工作流密钥.md?raw'; // 根据实际路径调整
import 推送器说明书 from '~/assets/md/推送器说明书.md?raw'; // 根据实际路径调整
import 告警管理使用手册 from '~/assets/md/告警管理使用手册.md?raw'; // 根据实际路径调整
// 折叠面板
const activeName = ref('')

const mdId1 = 'preview-only1';
const markdownContent1 = ref('');
const mdId2 = 'preview-only2';
const markdownContent2 = ref('');
const mdId3 = 'preview-only3';
const markdownContent3 = ref('');
// 加载 markdown 文本文件内容
const loadMarkdownContent = async () => {
  // const response = await fetch(平台说明书);
  markdownContent1.value = 如何获取工作流密钥;
  markdownContent2.value = 推送器说明书;
  markdownContent3.value = 告警管理使用手册;
};


const id = 'preview-only';
const text = ref<string>();
// 在组件挂载后加载并渲染 Markdown 内容
// 在组件挂载后加载文本文件内容，并在文本文件发生更改时重新加载
onMounted(() => {
  loadMarkdownContent();
});
</script>

<style scoped>
.preview {
  height: 600px;
}
.preview img {
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
  /*max-width: 50%;*/
}

.default-theme img {
  margin: 0 auto;
  max-width: 50%!important;
  box-sizing: border-box;
  padding: 5px;
  border: 1px solid var(--md-theme-border-color);
  border-radius: 3px;
}
</style>
