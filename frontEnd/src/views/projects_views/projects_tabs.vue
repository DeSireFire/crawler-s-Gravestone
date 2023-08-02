<template>
	<div class="container">
		<el-tabs v-model="ptabs">
			<el-tab-pane :label="`项目首页`" name="first">
        <sub_projectDetail v-if="pidExists" :pid="route.query.pid" :pname="route.query.name"/>
			</el-tab-pane>
			<el-tab-pane :label="`工作流定义`" name="second">
        <sub_workerLinks v-if="pidExists" :pid="route.query.pid" :pname="route.query.name"/>
        <span></span>
			</el-tab-pane>
			<el-tab-pane :label="`任务实例`" name="third">
        <sub_jobObj v-if="pidExists" :pid="route.query.pid" :pname="route.query.name"/>
        <span></span>
			</el-tab-pane>
		</el-tabs>
	</div>
</template>

<script setup lang="ts" name="projects_tabs">
import {useRoute} from 'vue-router';
import {ref, reactive, watchEffect} from 'vue';
import sub_projectDetail from './sub_projectDetail.vue';
import sub_workerLinks from './sub_workerLinks.vue';
import sub_jobObj from './sub_jobObj.vue';
const ptabs = ref('first');
// 获取当前路由
const route = useRoute();
// 使用 ref 来保存参数信息
const pidExists = ref(false);
watchEffect(() => {
  pidExists.value = 'pid' in route.query;
});
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
