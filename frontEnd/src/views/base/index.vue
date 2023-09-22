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
        <el-card shadow="hover" style="height: 507px">
          <template #header>
            <div class="clearfix">
              <span>日志统计</span>
              <el-button style="float: right; padding: 6px 0" text @click="getLogs()"> 刷新 </el-button>
            </div>
          </template>
          <el-tabs v-model="activeName" tab-position="left" class="job-log-tabs" @tab-click="handleClick">
            <!--     昨日统计 近7日统计 历史统计      -->
            <el-tab-pane label="昨日" name="first">
              <div v-if="dLogsTotal.yesterday.length">
                <div  v-for="(item, key) in dLogsTotal.yesterday">
                  <router-link
                      :to="
                  { path: '/projects_tabs', query: {
                    pid:item.pid,
                    name:item.pname,
                    title:item.pname,
                  }}">
                    <span class="folder-name">{{ item.wname }}</span>
                  </router-link>
                  <el-progress
                      :text-inside="true"
                      :stroke-width="20"
                      :percentage="floatToPercentage(item.log_proportion)"
                      :color="progressColor"
                  >
                    <span class="progress-content">{{ floatToPercentage(item.log_proportion) }}%:{{item.log_sum}} 条</span>
                  </el-progress>
                </div>
              </div>
              <div v-else class="no-data">暂无数据</div>
            </el-tab-pane>
            <el-tab-pane label="近7天" name="second">
              <div v-if="dLogsTotal.last_7_days.length">
                <div  v-for="(item, key) in dLogsTotal.last_7_days">
                  <router-link
                      :to="
                  { path: '/projects_tabs', query: {
                    pid:item.pid,
                    name:item.pname,
                    title:item.pname,
                  }}">
                    <span class="folder-name">{{ item.wname }}</span>
                  </router-link>
                  <el-progress
                      :text-inside="true"
                      :stroke-width="20"
                      :percentage="floatToPercentage(item.log_proportion)"
                      :color="progressColor"
                  >
                    <span class="progress-content">{{ floatToPercentage(item.log_proportion) }}%:{{item.log_sum}} 条</span>
                  </el-progress>
                </div>
              </div>
              <div v-else class="no-data">暂无数据</div>
            </el-tab-pane>
            <el-tab-pane label="历史" name="third">
              <div v-if="dLogsTotal.all_time.length">
                <div  v-for="(item, key) in dLogsTotal.all_time">
                  <router-link
                      :to="
                  { path: '/projects_tabs', query: {
                    pid:item.pid,
                    name:item.pname,
                    title:item.pname,
                  }}">
                    <span class="folder-name">{{ item.wname }}</span>
                  </router-link>
                  <el-progress
                      :text-inside="true"
                      :stroke-width="20"
                      :percentage="floatToPercentage(item.log_proportion)"
                      :color="progressColor"
                  >
                    <span class="progress-content">{{ floatToPercentage(item.log_proportion) }}%:{{item.log_sum}} 条</span>
                  </el-progress>
                </div>
              </div>
              <div v-else class="no-data">暂无数据</div>
            </el-tab-pane>
            <el-tab-pane label="大小比例" name="fourth">
              <div v-if="dLogsTotal.proportion.length">
                <div  v-for="(item, key) in dLogsTotal.proportion">
                  <span class="folder-name">{{ item.folder_name }}</span>
                  <el-progress
                      :text-inside="true"
                      :stroke-width="20"
                      :percentage="floatToPercentage(item.size_ratio)"
                      :color="progressColor"
                  >
                    <span class="progress-content"> {{ floatToPercentage(item.size_ratio) }}%:{{ item.size_human_readable }}</span>
                  </el-progress>
                </div>
              </div>
              <div v-else class="no-data">暂无数据</div>
            </el-tab-pane>
          </el-tabs>
        </el-card>
      </el-col>
      <el-col :span="16">
        <el-row :gutter="20" class="mgb20">
          <el-col :span="8">
            <el-card shadow="hover" :body-style="{ padding: '0px' }">
              <div class="grid-content grid-con-1">
                <el-icon class="grid-con-icon"><MessageBox /></el-icon>
                <div class="grid-cont-right">
                  <div class="grid-num">{{ board_info.project_total }}</div>
                  <div>项目总数</div>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card shadow="hover" :body-style="{ padding: '0px' }">
              <div class="grid-content grid-con-1">
                <el-icon class="grid-con-icon"><Document /></el-icon>
                <div class="grid-cont-right">
                  <div class="grid-num">{{ board_info.logger_total }}</div>
                  <div>日志总量</div>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card shadow="hover" :body-style="{ padding: '0px' }">
              <div class="grid-content grid-con-1">
                <el-icon class="grid-con-icon"><Finished /></el-icon>
                <div class="grid-cont-right">
                  <div class="grid-num">{{ board_info.jobs_total }}</div>
                  <div>任务总数</div>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
        <el-row :gutter="20" class="mgb20">
          <el-col :span="8">
            <el-card shadow="hover" :body-style="{ padding: '0px' }">
              <div class="grid-content grid-con-2">
                <el-icon class="grid-con-icon"><DocumentChecked /></el-icon>
                <div class="grid-cont-right">
                  <div class="grid-num">{{ board_info.yesterday_finish_jobs }}</div>
                  <div>昨日任务完成</div>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card shadow="hover" :body-style="{ padding: '0px' }">
              <div class="grid-content grid-con-2">
                <el-icon class="grid-con-icon"><Document /></el-icon>
                <div class="grid-cont-right">
                  <div class="grid-num">{{ board_info.yesterday_new_logger }}</div>
                  <div>昨日日志数量</div>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card shadow="hover" :body-style="{ padding: '0px' }">
              <div class="grid-content grid-con-2">
                <el-icon class="grid-con-icon"><Connection /></el-icon>
                <div class="grid-cont-right">
                  <div class="grid-num">{{ board_info.working_jobs }}</div>
                  <div>当前执行任务</div>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
        <el-row :gutter="20" class="mgb20">
          <el-col :span="8">
<!--            <el-card shadow="hover" :body-style="{ padding: '0px' }">-->
<!--              <div class="grid-content grid-con-4">-->
<!--                <el-icon class="grid-con-icon"><Cpu /></el-icon>-->
<!--                <div class="grid-cont-right">-->
<!--                  <div class="grid-num">-->
<!--                    {{ board_info.taobao_captcha_api }}-->
<!--                  </div>-->
<!--                  <div>淘系调用总数</div>-->
<!--                </div>-->
<!--              </div>-->
<!--            </el-card>-->
            <el-card shadow="hover" :body-style="{ padding: '0px' }">
              <div class="grid-content grid-con-4">
                <el-icon class="grid-con-icon"><ElementPlus /></el-icon>
                <div class="grid-cont-right">
                  <div class="grid-num">{{ floatToPercentage(taobao_captcha_api.passing_rate) }}%</div>
                  <div>饿了么滑块接口</div>
                  <div>今日通过率</div>
                </div>
                <div class="grid-cont-info">
                  <div>通过数:  <span class="grid-info-num">{{ taobao_captcha_api.passing_total }}</span></div>
                  <div>失败数:  <span class="grid-info-num">{{ taobao_captcha_api.failure_total }}</span></div>
                  <div>今日总:  <span class="grid-info-num">{{ taobao_captcha_api.passing_total + taobao_captcha_api.failure_total }}</span></div>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card shadow="hover" :body-style="{ padding: '0px' }">
              <div class="grid-content grid-con-4">
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
              <div class="grid-content grid-con-4">
                <el-icon class="grid-con-icon"><Monitor /></el-icon>
                <div class="grid-cont-right">
                  <div class="grid-num">{{ board_info.disk_total }}</div>
                  <div>已用存储空间</div>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
        <el-card shadow="hover" style="height: 415px">
          <template #header>
            <div class="clearfix">
              <span>任务概览</span>
              <el-button style="float: right; padding: 6px 0" text @click="getDJobs()"> 刷新 </el-button>
            </div>
          </template>
          <el-table :show-header="false" :data="todoList" style="width: 100%">
            <el-table-column :show-overflow-tooltip="true">
              <template #default="scope">
                <div class="todo-item">
                  <router-link :to="
                  { path: '/jobObjs', query: {
                    name:scope.row.name,
                  }}"> {{ scope.row.title }}...
                  </router-link>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="datetime" width="250">
              <template #default="scope">
                <div class="todo-item">
                  结束时间: {{ scope.row.datetime }}
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="datetime" width="250" :show-overflow-tooltip="true">
              <template #default="scope">
                <div class="todo-item">
                  耗时: {{ scope.row.duration }}
                </div>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts" name="system_dashboard">
import Schart from 'vue-schart';
import {onBeforeMount, reactive, ref} from 'vue';
// import imgurl from '../assets/img/img.jpg';
// import {get_ip_info} from '~/api';
import { ipInfo } from '~/api/extras';
import {fetchChartss} from "~/api";
import {getDashInfo, getDashJobs, getDashLogs, getDashTB} from "~/api/dashboard";
import type { TabsPaneContext } from 'element-plus'
const activeName = ref('first')
const handleClick = (tab: TabsPaneContext, event: Event) => {
  console.log(tab, event)
}
const imgurl = 'https://avatars.githubusercontent.com/u/64947085?v=4'

const name = localStorage.getItem('ms_username');
const role: string = name === 'admin' ? '超级管理员' : '普通用户';
const local_name = ref('未知');
const formattedDate = ref('未知');

const board_info = reactive({
  // 用户总数
  user_total: '--',
  // 程序总数
  programs_total: '--',
  // 日志总量
  logger_total: '--',
  // 项目总量
  project_total: '--',

  // 待定
  system_info: '--',
  // 内存占用
  memory_total: '--',
  // cpu占用
  master_cpu: '--',

  // 昨日任务完成
  yesterday_finish_jobs: '--',
  // 昨日任务数量
  yesterday_new_logger: '--',
  // 当前执行任务
  working_jobs: '--',
  // 任务总数
  jobs_total: '--',
  // 硬盘占用
  disk_total: '--',
})

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
  local_name.value = result.data?.data?.city ?? result.data?.regionName;
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

  board_info.yesterday_finish_jobs = result.data.yesterday_finish_jobs;
  board_info.yesterday_new_logger = result.data.yesterday_new_logger;
  board_info.working_jobs = result.data.working_jobs;
  board_info.jobs_total = result.data.jobs_total;
  board_info.disk_total = `${floatToPercentage(result.data.disk_total)}%`;
};
getBoard();

interface tbCaptchaTotal {
  pid: string;
  wid: string;
  jid: string;
  job_name: string;
  passing_total: number;
  failure_total: number;
  passing_rate: number;
  history_total: number;
}


// 淘系接口统计信息
const taobao_captcha_api = ref(<tbCaptchaTotal>{})
const getTBTotal = async () => {
  const result = (await getDashTB());
  taobao_captcha_api.value = result.data
};
getTBTotal();

// 获取仪表盘任务概览信息
interface djobsItem {
  id: string;
  name: string;
  status: string;
  datetime: string;
  title: string;
  duration: string;
}
const todoList = ref<djobsItem[]>([]);
const getDJobs = async () => {
  const result = (await getDashJobs())
  todoList.value = result.data.list;
};
getDJobs()

// 日志比例信息
const progressColor = [
  { color: '#6f7ad3', percentage: 10 },
  { color: '#1989fa', percentage: 20 },
  { color: '#5cb87a', percentage: 30 },
  { color: '#e6a23c', percentage: 40 },
  { color: '#f56c6c', percentage: 50 },
]

interface LogEntry {
  wid: string;
  pid: string;
  wname: string;
  pname: string;
  log_sum: number;
  log_proportion: number;
}

interface ProportionFolder {
  folder_name: string;
  size_bytes: number;
  size_human_readable: string;
  size_ratio: number;
}

const dLogsTotal = reactive({
  yesterday: <LogEntry[]>([]),
  last_7_days: <LogEntry[]>([]),
  all_time: <LogEntry[]>([]),
  proportion: <ProportionFolder[]>([]),
})


const getLogs = async () => {
  const result = (await getDashLogs())
  dLogsTotal.yesterday = result.data.yesterday;
  dLogsTotal.last_7_days = result.data.last_7_days;
  dLogsTotal.all_time = result.data.all_time;
  dLogsTotal.proportion = result.data.proportion;
};
getLogs()


// 浮点数转为百分比
function floatToPercentage(value: number): number {
  // 将浮点数转换为百分比形式，保留两位小数并四舍五入
  return parseFloat((value * 100).toFixed(2));
}


// 为数据项选择颜色
function getRandomColor(): string {
  const letters = "0123456789ABCDEF";
  let color = "#";
  for (let i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}


onBeforeMount(() => {
  // getLocal()
})
</script>

<style scoped>
.progress-content {
  color: #2c0b0b
}

.job-log-tabs > .el-tabs__content {
  padding: 32px;
  color: #6b778c;
  font-size: 32px;
  font-weight: 600;
}

.folder-name {
  flex: 1;
  margin-right: 10px;
}

.no-data {
  display: flex;
  height: 200px;
  justify-content: center;
  align-items: center;
  /*height: 100%;*/
  color: #999;
}

.el-row {
  margin-bottom: 20px;
}

.el-row a{
  color: #303133;
}
.el-row a.router-link-exact-active {
  color: #73767a; /* 设置你想要的字体颜色 */
}

.grid-content {
  display: flex;
  align-items: center;
  height: 100px;
}

.grid-cont-info {
  border-left: 1px dotted #999;
  flex: 1;
  font-size: 10px;
  color: #999;
  padding: 5px 10px 5px 10px;
}

.grid-info-num {
  font-size: 20px;
  font-weight: bold;
}

.grid-cont-right {
  flex: 1;
  text-align: center;
  font-size: 10px;
  color: #999;
}

.grid-num {
  font-size: 20px;
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
  background: #409eff;
}

.grid-con-1 .grid-num {
  color: #409eff;
}

.grid-con-1 .grid-info-num {
  color: #409eff;
}


.grid-con-2 .grid-con-icon {
  background: #33CC99;
}

.grid-con-2 .grid-num {
  color: #33CC99;
}

.grid-con-2 .grid-info-num {
  color: #33CC99;
}

.grid-con-3 .grid-con-icon {
  background: #FF6666;
}

.grid-con-3 .grid-info-num {
  color: #FF6666;
}

.grid-con-3 .grid-num {
  color: #FF6666;
}

.grid-con-4 .grid-con-icon {
  background: #FF9966;
}

.grid-con-4 .grid-info-num {
  color: #FF9966;
}

.grid-con-4 .grid-num {
  color: #FF9966;
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
