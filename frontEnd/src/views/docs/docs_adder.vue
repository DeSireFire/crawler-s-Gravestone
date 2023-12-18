<template>
  <div class="container">
    <div class="plugins-tips">
      <b>知识星球-文档新建</b>
    </div>
    <div class="container">
      <MdPreview :editorId="mdId" :modelValue="valueHtml" />
    </div>
    <el-divider border-style="dashed" />
    <div class="title-box">
      <el-input v-model="content.title" placeholder="输入文章标题..." class="mr10"/>
    </div>
    <br>
    <div style="border: 1px solid #ccc">
      <Toolbar
          style="border-bottom: 1px solid #ccc"
          :editor="editorRef"
          :defaultConfig="toolbarConfig"
      />
      <Editor
          style="height: 500px; overflow-y: hidden;"
          v-model="valueHtml"
          :defaultConfig="editorConfig"
          @onCreated="handleCreated"
      />
<!--      <Editor-->
<!--          @onCreated="handleCreated"-->
<!--          @onChange="handleChange"-->
<!--          @onDestroyed="handleDestroyed"-->
<!--          @onFocus="handleFocus"-->
<!--          @onBlur="handleBlur"-->
<!--          @customAlert="customAlert"-->
<!--          @customPaste="customPaste"-->
<!--      />-->
    </div>
    <br>
    <el-button type="primary" @click="syncHTML">提交</el-button>
  </div>
</template>

<script setup lang="ts" name="docs_editor">
import 'md-editor-v3/lib/preview.css';
import '@wangeditor/editor/dist/css/style.css' // 引入 css
import {ref, reactive, onMounted, onBeforeUnmount, shallowRef, watch} from 'vue';
import { MdPreview,MdEditor, MdCatalog } from 'md-editor-v3';
import { Editor, Toolbar } from '@wangeditor/editor-for-vue'
import { convertHtmlToMarkdown } from "~/store/docs";
import {updateDoc} from "~/api/docs";
import {ElMessage} from "element-plus";
import {useRoute, useRouter} from "vue-router";

const name = localStorage.getItem('ms_username');
const mdId = 'preview-only';

// 编辑器实例，必须用 shallowRef
const editorRef = shallowRef()

// 内容 HTML
const content = reactive({
  doc_id: '',
  title: '',
  author: name,
  content: '',
  md_content: '',
  desc: '',
});
const valueHtml = ref('<h1>Hello, World!</h1><p>This is <strong>bold</strong> text.</p>')

// 获取路由对象
const route = useRoute();
const router = useRouter();
const back = ref(route.query.back||'');
const title = ref(route.query.title||'');
const author = ref(route.query.author||'');
const doc_id = ref(route.query.doc_id||'');

// // 使用 ref 来保存参数信息
// const logExists = ref(false);
// // 监听路由参数的变化
// watch(() => route.query, (newParam, oldParam) => {
//   // 如果跳出日志详情页面，则不再执行往后的内容
//   const currentPath = route.path;
//   logExists.value = '/docs_editor' === currentPath;
//   if (logExists.value) {
//   }
// });

// 模拟 ajax 异步获取内容
onMounted(() => {
  const route = useRoute();
  const router = useRouter();
  const doc_id = ref(route.query.doc_id||'');
  console.log("doc_id", doc_id.value)

  // setTimeout(() => {
  //   valueHtml.value = ''
  // }, 1500)
  // if (doc_id) {
  //   console.log("doc_id", doc_id.value)
  // }
})

const toolbarConfig = {}
const editorConfig = {
  preview: true,
  mode: 'default',
  placeholder: '请输入内容...',
}

// 组件销毁时，也及时销毁编辑器
onBeforeUnmount(() => {
  const editor = editorRef.value
  if (editor == null) return
  editor.destroy()
})

const handleCreated = (editor: any) => {
  editorRef.value = editor // 记录 editor 实例，重要！
}

const truncateText = (text:string, maxLength:number) => {
  if (text.length > maxLength) {
    return text.slice(0, maxLength - 3) + '...';
  }
  return text;
}

const syncHTML = async () => {
  content.content = valueHtml.value;
  // 转为markdown方便保存时做文本查询
  const md_c = convertHtmlToMarkdown(valueHtml.value);
  console.log("md_c", md_c)
  content.md_content = md_c;

  // 根据文本内容创建建议描述
  // content.desc = ""
  // content.desc = truncateText(convertHtmlToMarkdown(valueHtml.value), 10);
  // console.log("md_c", content.desc)

  // 向后端发起操作
  const response = (await updateDoc(content));
  if (response.isSuccess) {
    ElMessage.success(`保存 ${content.title} 成功！`);
  } else {
    ElMessage.error(`新增 ${content.title} 失败！`);
  }
};

</script>

<style scoped>
.title-box {
  margin-top: 20px;
}

</style>
