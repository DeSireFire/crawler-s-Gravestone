<template>
  <div class="container">
    <div class="plugins-tips">
      <b>知识星球-文档编辑</b>
    </div>
    <div class="container">
      <MdPreview :editorId="mdId" :modelValue="mainContent" />
    </div>
    <el-divider border-style="dashed" />
    <div class="title-box">
      <el-input v-model="doc.title" placeholder="输入文章标题..." class="mr10"/>
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
          v-model="mainContent"
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
<!--    <el-button type="primary" @click="syncHTML">提交</el-button>-->
  </div>
</template>

<script setup lang="ts" name="docs_editor">
import 'md-editor-v3/lib/preview.css';
import '@wangeditor/editor/dist/css/style.css' // 引入 css
import {ref, reactive, onMounted, onBeforeUnmount, shallowRef, watch} from 'vue';
import { MdPreview,MdEditor, MdCatalog } from 'md-editor-v3';
import { Editor, Toolbar } from '@wangeditor/editor-for-vue'
import { convertHtmlToMarkdown } from "~/store/docs";
import {getDoc, updateDoc} from "~/api/docs";
import {ElMessage} from "element-plus";
import {useRoute, useRouter} from "vue-router";

// 配置变量
const mdId = 'preview-only';
const toolbarConfig = {}
const editorConfig = {
  preview: true,
  mode: 'default',
  placeholder: '请输入内容...',
}
// 编辑器实例，必须用 shallowRef
const editorRef = shallowRef()
// 声明
const name = localStorage.getItem('ms_username');
// 获取路由对象
const route = useRoute();
const router = useRouter();
const back = ref(route.query.back||'');
const title = ref(route.query.title||'');
const author = ref(route.query.author||'');
const doc_id = ref(route.query.doc_id||'');

// 请求信息
const doc_params = reactive({
  doc_id:'',
  title: '',
  reader: name,
})
// 文档信息
const doc = reactive({
  id: '',
  article_source: '',
  author: '',
  author_id: '',
  doc_id: '',
  title: '',
  content: '',
  md_content: '',
  desc: '',
  create_time: '',
  extra: '',
  reading_permissions: '',
  update_time: '',
});
// 内容 HTML
const content = reactive({
  doc_id: '',
  title: '',
  author: name,
  content: '',
  md_content: '',
  desc: '',
});
const mainContent = ref('')
// 组件销毁时，也及时销毁编辑器
onBeforeUnmount(() => {
  const editor = editorRef.value
  if (editor == null) return
  editor.destroy()
})

const handleCreated = (editor: any) => {
  editorRef.value = editor // 记录 editor 实例，重要！
}

// 使用 ref 来保存参数信息
const Exists = ref(false);
// 监听路由参数的变化
watch(() => route.query, (newPid, oldPid) => {
  // 如果跳出文章阅读页面，则不再执行往后的内容
  const currentPath = route.path;
  Exists.value = '/docs_previwer' === currentPath;
  if (Exists.value) {
    console.log("currentPath",currentPath)
    handleDocsInfo();
    handleDocContent();
  }
});
// 获取文章信息
const handleDocsInfo = () => {
  // (a === null || a !== b)
  const urlParams = new URLSearchParams(window.location.hash.split('?')[1]);
  doc_id.value = urlParams.get('doc_id') || '' as string;
  doc_params.doc_id = urlParams.get('doc_id') || '' as string;
  doc_params.title = urlParams.get('title') || '' as string;
};
const handleDocContent = async () => {
  handleDocsInfo();
  // 获取文档内容
  const response = (await getDoc(doc_params))
  doc.article_source = response.data.doc.article_source
  doc.author = response.data.doc.author
  doc.author_id = response.data.doc.author_id
  doc.content = response.data.doc.content
  doc.create_time = response.data.doc.create_time
  doc.desc = response.data.doc.desc
  doc.doc_id = response.data.doc.doc_id
  doc.extra = response.data.doc.extra
  doc.id = response.data.doc.id
  doc.md_content = response.data.doc.md_content
  doc.reading_permissions = response.data.doc.reading_permissions
  doc.title = response.data.doc.title
  doc.update_time = response.data.doc.update_time
  mainContent.value = doc.content

  if (response.isSuccess) {
    ElMessage.success(`刷新 ${doc.title} 成功！`);
  } else {
    ElMessage.error(`加载 ${doc_params.title} 失败！`);
  }
}

const syncHTML = async () => {
  content.content = mainContent.value;
  // 转为markdown方便保存时做文本查询
  const md_c = convertHtmlToMarkdown(mainContent.value) as string;
  content.md_content = md_c;

  // 向后端发起操作
  const response = (await updateDoc(content));
  if (response.isSuccess) {
    ElMessage.success(`保存 ${content.title} 成功！`);
  } else {
    ElMessage.error(`保存 ${content.title} 失败！`);
  }
};

// 异步文档内容
onMounted(() => {
  handleDocContent();
})
</script>

<style scoped>
.title-box {
  margin-top: 20px;
}

</style>
