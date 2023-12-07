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
import {updateDoc} from "~/api/docs";
import {ElMessage} from "element-plus";
import {useRoute, useRouter} from "vue-router";


const markdownText = ref('');

const mdId = 'preview-only';

// 编辑器实例，必须用 shallowRef
const editorRef = shallowRef()

// 内容 HTML
const content = reactive({
  doc_id: '',
  title: '',
  content: '',
  md_content: '',
  desc: '',
});
const route = useRoute();
const router = useRouter();
const valueHtml = ref('hello world')
const doc_id = ref(route.query.doc_id||'');
const handleDocsInfo = () => {
  const urlParams = new URLSearchParams(window.location.hash.split('?')[1]);
  doc_id.value = urlParams.get('doc_id') as string;
};

// 使用 ref 来保存参数信息
const Exists = ref(false);
// 监听路由参数的变化
watch(() => route.query, (newPid, oldPid) => {
  // 如果跳出日志详情页面，则不再执行往后的内容
  const currentPath = route.path;
  Exists.value = '/docs_previwer' === currentPath;
  if (Exists.value) {
    handleDocsInfo();
  }
});

// 模拟 ajax 异步获取内容
onMounted(() => {
  console.log("doc_id", doc_id.value)


  // setTimeout(() => {
  //   valueHtml.value = ''
  // }, 1500)
})

// const syncHTML = async () => {
//   content.content = valueHtml.value;
//   // 转为markdown方便保存时做文本查询
//   const md_c = convertHtmlToMarkdown(valueHtml.value);
//   console.log("md_c", md_c)
//   content.md_content = md_c;
//
//   // 向后端发起操作
//   const response = (await updateDoc(content));
//   if (response.isSuccess) {
//     ElMessage.success(`保存 ${content.title} 成功！`);
//   } else {
//     ElMessage.error(`新增 ${content.title} 失败！`);
//   }
// };

</script>

<style scoped>
.title-box {
  margin-top: 20px;
}

</style>
