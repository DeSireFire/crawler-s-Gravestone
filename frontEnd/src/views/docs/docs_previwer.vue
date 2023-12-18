<template>
  <div class="container">
    <div class="plugins-tips">
      <b>知识星球-文档阅读</b>
    </div>
    <div class="container">
      <MdPreview :editorId="mdId" :modelValue="markdownText" />
    </div>
  </div>
</template>

<script setup lang="ts" name="docs_previwer">
import 'md-editor-v3/lib/preview.css';
import '@wangeditor/editor/dist/css/style.css' // 引入 css
import {ref, reactive, onMounted, onBeforeUnmount, shallowRef, watch} from 'vue';
import { MdPreview,MdEditor, MdCatalog } from 'md-editor-v3';
import {getDoc} from "~/api/docs";
import {ElMessage} from "element-plus";
import {useRoute, useRouter} from "vue-router";

const name = localStorage.getItem('ms_username');
const markdownText = ref('');

const mdId = 'preview-only';

// 编辑器实例，必须用 shallowRef
const editorRef = shallowRef()

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
const route = useRoute();
const router = useRouter();
const doc_id = ref(route.query.doc_id||'');
const handleDocsInfo = () => {
  // (a === null || a !== b)
  const urlParams = new URLSearchParams(window.location.hash.split('?')[1]);
  doc_id.value = urlParams.get('doc_id') || '' as string;
  doc_params.doc_id = urlParams.get('doc_id') || '' as string;
  doc_params.title = urlParams.get('title') || '' as string;
};

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

// 模拟 ajax 异步获取内容
onMounted(() => {
  handleDocContent();
})

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
  markdownText.value = doc.content

    if (response.isSuccess) {
    ElMessage.success(`刷新 ${doc.title} 成功！`);
  } else {
    ElMessage.error(`加载 ${doc_params.title} 失败！`);
  }
}

</script>

<style scoped>
.title-box {
  margin-top: 20px;
}

</style>
