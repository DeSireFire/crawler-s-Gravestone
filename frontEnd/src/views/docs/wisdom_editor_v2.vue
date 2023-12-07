<template>
  <div class="container">
    <div class="plugins-tips">
      <b>知识星球-文档编辑</b>
    </div>
    <div class="mgb20" ref="editor"></div>
    <MdEditor class="mgb20" ref="editor" v-model="text" @on-upload-img="onUploadImg" />
    <el-button type="primary" @click="syncHTML">提交</el-button>
  </div>
</template>

<script setup lang="ts" name="editor">
import WangEditor from 'wangeditor';
import { ref, reactive, onMounted, onBeforeUnmount } from 'vue';

const editor = ref(null);
const content = reactive({
  html: '',
  text: ''
});
let instance: any;
onMounted(() => {
  instance = new WangEditor(editor.value);
  instance.config.zIndex = 1;
  instance.create();
});
onBeforeUnmount(() => {
  instance.destroy();
  instance = null;
});
const syncHTML = () => {
  content.html = instance.txt.html();
  console.log(content.html);
};
const onUploadImg = (files: any) => {
  console.log(files);
};
</script>

<style></style>
