<template>
	<div class="container">
		<div class="plugins-tips">
      <b>使用文档(开发中..)</b>
		</div>
	</div>
</template>

<script setup lang="ts" name="md">
import { ref } from 'vue';
import { MdEditor } from 'md-editor-v3';
import 'md-editor-v3/lib/style.css';
const text = ref('Hello Editor!');
const onUploadImg = (files: any) => {
	console.log(files);
};
</script>
