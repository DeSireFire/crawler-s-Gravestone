<template>
	<div>
		<el-row :gutter="20">
			<el-col :span="8">
				<el-card shadow="hover" class="mgb20" style="height: 252px">
					<div class="user-info">
						<el-avatar :size="120" :src="imgurl" />
						<div class="user-info-cont">
							<div class="user-info-name">{{ name }}</div>
							<div>{{ role }}</div>
						</div>
					</div>
					<div class="user-info-list">
						上次登录时间：
						<span>{{ formattedDate }}</span>
					</div>
					<div class="user-info-list">
						上次登录地点：
						<span>{{ local_name }}</span>
					</div>
				</el-card>
<!--				<el-card shadow="hover" style="height: auto">-->
<!--					<template #header>-->
<!--						<div class="clearfix">-->
<!--							<span>日志比例Top5</span>-->
<!--						</div>-->
<!--					</template>-->
<!--					高德地图-->
<!--					<el-progress :percentage="69.4" color="#42b983"></el-progress>-->
<!--					企查查-->
<!--					<el-progress :percentage="14" color="#f1e05a"></el-progress>-->
<!--					美团-->
<!--					<el-progress :percentage="5.6"></el-progress>-->
<!--					药监局-->
<!--					<el-progress :percentage="9" color="#f56c6c"></el-progress>-->
<!--          饿了么-->
<!--          <el-progress :percentage="1" color="#f56c6c"></el-progress>-->
<!--				</el-card>-->
			</el-col>
			<el-col :span="16">
				<el-row :gutter="20" class="mgb20">
          <el-col :span="8">
            <el-card shadow="hover" :body-style="{ padding: '0px' }">
              <div class="grid-content grid-con-2">
                <el-icon class="grid-con-icon"><ChatDotRound /></el-icon>
                <div class="grid-cont-right">
                  <div class="grid-num">{{ board_info.project_total }}</div>
                  <div>项目数量</div>
                </div>
              </div>
            </el-card>
          </el-col>
					<el-col :span="8">
						<el-card shadow="hover" :body-style="{ padding: '0px' }">
							<div class="grid-content grid-con-2">
								<el-icon class="grid-con-icon"><ChatDotRound /></el-icon>
								<div class="grid-cont-right">
									<div class="grid-num">{{ board_info.programs_total }}</div>
									<div>程序数量</div>
								</div>
							</div>
						</el-card>
					</el-col>
					<el-col :span="8">
						<el-card shadow="hover" :body-style="{ padding: '0px' }">
							<div class="grid-content grid-con-3">
								<el-icon class="grid-con-icon"><Document /></el-icon>
								<div class="grid-cont-right">
									<div class="grid-num">{{ board_info.logger_total }}</div>
									<div>日志数量</div>
								</div>
							</div>
						</el-card>
					</el-col>
				</el-row>
				<el-row :gutter="20" class="mgb20">
          <el-col :span="8">
            <el-card shadow="hover" :body-style="{ padding: '0px' }">
              <div class="grid-content grid-con-1">
                <el-icon class="grid-con-icon"><User /></el-icon>
                <div class="grid-cont-right">
                  <div class="grid-num">{{ board_info.user_total }}</div>
                  <div>用户数量</div>
                </div>
              </div>
            </el-card>
          </el-col>
					<el-col :span="8">
						<el-card shadow="hover" :body-style="{ padding: '0px' }">
							<div class="grid-content grid-con-3">
								<el-icon class="grid-con-icon"><Cpu /></el-icon>
								<div class="grid-cont-right">
									<div class="grid-num">{{ board_info.master_cpu }} %</div>
									<div>CPU负载</div>
								</div>
							</div>
						</el-card>
					</el-col>
					<el-col :span="8">
						<el-card shadow="hover" :body-style="{ padding: '0px' }">
							<div class="grid-content grid-con-3">
<!--								<el-icon class="grid-con-icon"><Odometer /></el-icon>-->
								<el-icon class="grid-con-icon"><PieChart /></el-icon>
								<div class="grid-cont-right">
									<div class="grid-num">{{ board_info.memory_total }}</div>
									<div>内存占用</div>
								</div>
							</div>
						</el-card>
					</el-col>
<!--          <el-col :span="8">-->
<!--            <el-card shadow="hover" :body-style="{ padding: '0px' }">-->
<!--              <div class="grid-content grid-con-3">-->
<!--                <el-icon class="grid-con-icon"><DocumentDelete /></el-icon>-->
<!--                <div class="grid-cont-right">-->
<!--                  <div class="grid-num">{{ board_info.user_total }}</div>-->
<!--                  <div>失败合计</div>-->
<!--                </div>-->
<!--              </div>-->
<!--            </el-card>-->
<!--          </el-col>-->
				</el-row>
				<el-card shadow="hover" style="height: 403px">
					<template #header>
						<div class="clearfix">
							<span>待办事项</span>
							<el-button style="float: right; padding: 3px 0" text>添加</el-button>
						</div>
					</template>

					<el-table :show-header="false" :data="todoList" style="width: 100%">
						<el-table-column width="40">
							<template #default="scope">
								<el-checkbox v-model="scope.row.status"></el-checkbox>
							</template>
						</el-table-column>
						<el-table-column>
							<template #default="scope">
								<div
									class="todo-item"
									:class="{
										'todo-item-del': scope.row.status
									}"
								>
									{{ scope.row.title }}
								</div>
							</template>
						</el-table-column>
					</el-table>
				</el-card>
			</el-col>
		</el-row>
	</div>
</template>

<script setup lang="ts" name="dashboard">
import Schart from 'vue-schart';
import {onBeforeMount, reactive, ref} from 'vue';
// import imgurl from '../assets/img/img.jpg';
// import {get_ip_info} from '../../src/api';
import { ipInfo } from '~/api/extras';
import {fetchChartss} from "~/api";
import {getDashInfo} from "~/api/dashboard";
const imgurl = 'https://avatars.githubusercontent.com/u/64947085?v=4'

const name = localStorage.getItem('ms_username');
const role: string = name === 'admin' ? '超级管理员' : '普通用户';
const local_name = ref('未知');
const formattedDate = ref('未知');
const board_info = reactive({
  user_total: '--',
  system_info: '--',
  programs_total: '--',
  logger_total: '--',
  project_total: '--',
  memory_total: '--',
  master_cpu: '--',
});

// 当前日期格式化
const getDate = async () => {
const today = new Date();
const year = today.getFullYear();
const month = (today.getMonth() + 1).toString().padStart(2, '0');
const day = today.getDate().toString().padStart(2, '0');
formattedDate.value = `${year}-${month}-${day}` as string;
};
getDate()

// 获取登录ip地区
const getLocal = async () => {
  const result = await ipInfo();
  // console.log('result',result);
  local_name.value = result.data?.data?.city;
};
getLocal()

// 获取仪表盘基础信息
const getBoard = async () => {
  const result = (await getDashInfo())
  board_info.user_total = result.data.user_total;
  board_info.system_info = result.data.system_info;
  board_info.programs_total = result.data.programs_total;
  board_info.logger_total = result.data.logger_total;
  board_info.project_total = result.data.project_total;
  board_info.master_cpu = result.data.master_cpu;
  board_info.memory_total = result.data.memory_total;
};
getBoard()



const todoList = reactive([
	{
		title: '模拟数据3...',
		status: false
	},
	{
		title: '模拟数据2...',
		status: true
	},
	{
		title: '模拟数据1...',
		status: true
	}
]);

onBeforeMount(() => {
  // getLocal()
})
</script>

<style scoped>
.el-row {
	margin-bottom: 20px;
}

.grid-content {
	display: flex;
	align-items: center;
	height: 100px;
}

.grid-cont-right {
	flex: 1;
	text-align: center;
	font-size: 14px;
	color: #999;
}

.grid-num {
	font-size: 30px;
	font-weight: bold;
}

.grid-con-icon {
	font-size: 50px;
	width: 100px;
	height: 100px;
	text-align: center;
	line-height: 100px;
	color: #fff;
}

.grid-con-1 .grid-con-icon {
	background: rgb(45, 140, 240);
}

.grid-con-1 .grid-num {
	color: rgb(45, 140, 240);
}

.grid-con-2 .grid-con-icon {
	background: rgb(100, 213, 114);
}

.grid-con-2 .grid-num {
	color: rgb(100, 213, 114);
}

.grid-con-3 .grid-con-icon {
	background: rgb(242, 94, 67);
}

.grid-con-3 .grid-num {
	color: rgb(242, 94, 67);
}

.user-info {
	display: flex;
	align-items: center;
	padding-bottom: 20px;
	border-bottom: 2px solid #ccc;
	margin-bottom: 20px;
}

.user-info-cont {
	padding-left: 50px;
	flex: 1;
	font-size: 14px;
	color: #999;
}

.user-info-cont div:first-child {
	font-size: 30px;
	color: #222;
}

.user-info-list {
	font-size: 14px;
	color: #999;
	line-height: 25px;
}

.user-info-list span {
	margin-left: 70px;
}

.mgb20 {
	margin-bottom: 20px;
}

.todo-item {
	font-size: 14px;
}

.todo-item-del {
	text-decoration: line-through;
	color: #999;
}

.schart {
	width: 100%;
	height: 300px;
}
</style>
