<template>
	<div class="container">
<!--		<el-tabs v-model="ptabs" @tab-click="handleClick">-->
		<el-tabs v-model="ptabs">
			<el-tab-pane :label="`项目首页`" name="first">
        <sub_projectDetail />
			</el-tab-pane>
			<el-tab-pane :label="`工作流定义`" name="second">
        <sub_workerLinks />
			</el-tab-pane>
			<el-tab-pane :label="`任务实例`" name="third">
        <sub_jobObj />
			</el-tab-pane>
		</el-tabs>
	</div>
</template>

<script setup lang="ts" name="projects_tabs">
import {ref, reactive, onBeforeMount} from 'vue';
import sub_projectDetail from './sub_projectDetail.vue';
import sub_workerLinks from './sub_workerLinks.vue';
import sub_jobObj from './sub_jobObj.vue';
const ptabs = ref('first');
let project_info = reactive({
  pid: '',
  name: '',
  author: '',
  description: '',
});
let params_info = {};
const pid = ref('');
const handleProjectInfo = () => {
  const urlParams = new URLSearchParams(window.location.hash.split('?')[1]);
  pid.value = urlParams.get('pid') as string;
  params_info = Object.fromEntries(urlParams.entries());
};
handleProjectInfo();
// console.log(pid)
const handleClick = (tab:any, event:any) => {
  //这样才能获取每个el-tab-pane的name属性
  console.log(tab.props.name);
}
</script>

<style>
.message-title {
	cursor: pointer;
}
.handle-row {
	margin-top: 30px;
}
</style>
