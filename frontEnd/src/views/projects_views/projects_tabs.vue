<template>
	<div class="container">
		<el-tabs v-model="message">
			<el-tab-pane :label="`项目首页`" name="first">
        <el-row>
          <el-col :span="11">
            <el-table :data="state.unread" :show-header="false" style="width: 100%">
              <el-table-column>
                <template #default="scope">
                  <span class="message-title">{{ scope.row.title }}</span>
                </template>
              </el-table-column>
              <el-table-column prop="date" width="180"></el-table-column>
            </el-table>
          </el-col>
          <el-col :span="1"></el-col>
          <el-col :span="11">
            <el-table :data="state.unread" :show-header="false" style="width: 100%">
              <el-table-column>
                <template #default="scope">
                  <span class="message-title">{{ scope.row.title }}</span>
                </template>
              </el-table-column>
              <el-table-column prop="date" width="180"></el-table-column>
              <el-table-column width="120">
                <template #default="scope">
                  <el-button size="small" @click="handleRead(scope.$index)">标为已读</el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-col>
        </el-row>
				<div class="handle-row">
					<el-button type="primary">返回项目列表</el-button>
				</div>
			</el-tab-pane>
			<el-tab-pane :label="`工作流定义`" name="second">
        <sub_workerLinks></sub_workerLinks>
			</el-tab-pane>
			<el-tab-pane :label="`工作流状态`" name="third">
				<template v-if="message === 'third'">
          pass
				</template>
			</el-tab-pane>
			<el-tab-pane :label="`任务实例`" name="fourth">
				<template v-if="message === 'fourth'">
          pass
				</template>
			</el-tab-pane>
		</el-tabs>
	</div>
</template>

<script setup lang="ts" name="projects_tabs">
import { ref, reactive } from 'vue';
import sub_workerLinks from './sub_workerLinks.vue';
const message = ref('first');
let project_info = reactive({
  pid: '',
  name: '',
  author: '',
  description: '',
});
let params_info = {};
const pid = ref('');
const state = reactive({
	unread: [
		{
			date: '2023-07-20 20:00:00',
			title: '【系统通知】该系统将于今晚凌晨2点到5点进行升级维护'
		},
		{
			date: '2023-07-20 21:00:00',
			title: '今晚12点整发大红包，先到先得'
		}
	],
	read: [
		{
			date: '2023-07-20 20:00:00',
			title: '【系统通知】该系统将于今晚凌晨2点到5点进行升级维护'
		}
	],
	recycle: [
		{
			date: '2023-07-20 20:00:00',
			title: '【系统通知】该系统将于今晚凌晨2点到5点进行升级维护'
		}
	]
});
const handleProjectInfo = () => {
  const urlParams = new URLSearchParams(window.location.hash.split('?')[1]);
  pid.value = urlParams.get('pid') as string;
  params_info = Object.fromEntries(urlParams.entries());
};
handleProjectInfo();

// const handleRead = (index: number) => {
// 	const item = state.unread.splice(index, 1);
// 	state.read = item.concat(state.read);
// };
// const handleDel = (index: number) => {
// 	const item = state.read.splice(index, 1);
// 	state.recycle = item.concat(state.recycle);
// };
// const handleRestore = (index: number) => {
// 	const item = state.recycle.splice(index, 1);
// 	state.read = item.concat(state.read);
// };
</script>

<style>
.message-title {
	cursor: pointer;
}
.handle-row {
	margin-top: 30px;
}
</style>
