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
        <el-card shadow="hover" style="height: 373px">
          <template #header>
            <div class="clearfix">
              <span>日志比例Top</span>
              <el-button style="float: right; padding: 6px 0" text @click="getLogs()"> 刷新 </el-button>
            </div>
          </template>
          <div v-if="dlogs.length">
            <div  v-for="(item, key) in dlogs" v-if="dlogs.length">
              <span class="folder-name">{{ item.folder_name }}</span>
              <el-progress :percentage="floatToPercentage(item.size_ratio)" :color="getRandomColor()"></el-progress>
            </div>
          </div>
          <div v-else class="no-data">暂无数据</div>
        </el-card>
      </el-col>
      <el-col :span="16">
        <el-row :gutter="20" class="mgb20">
          <el-col :span="8">
            <el-card shadow="hover" :body-style="{ padding: '0px' }">
              <div class="grid-content grid-con-2">
                <el-icon class="grid-con-icon"><CreditCard /></el-icon>
                <div class="grid-cont-right">
                  <div class="grid-num">{{ board_info.project_total }}</div>
                  <div>项目数量</div>
                </div>
                <!--                <div class="grid-cont-info">-->
                <div class="grid-cont-right">
                  <div>项目数量:  <span class="grid-info-num">{{ board_info.project_total }}</span></div>
                  <div>项目数量:  <span class="grid-info-num">{{ board_info.project_total }}</span></div>
                  <div>项目数量:  <span class="grid-info-num">{{ board_info.project_total }}</span></div>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card shadow="hover" :body-style="{ padding: '0px' }">
              <div class="grid-content grid-con-2">
                <el-icon class="grid-con-icon"><Postcard /></el-icon>
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
import {getDashInfo, getDashJobs, getDashLogs} from "~/api/dashboard";
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
};
getBoard()

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
interface dlogsItem {
  folder_name: string;
  size_bytes: string;
  size_human_readable: string;
  size_ratio: number;
}
const dlogs = ref<dlogsItem[]>([]);
const getLogs = async () => {
  const result = (await getDashLogs())
  dlogs.value = result.data.list;
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

.grid-content {
  display: flex;
  align-items: center;
  height: 100px;
}

.grid-cont-info {
  font-size: 20px;
  color: #999;
  padding: 5px 5px 5px 20px;
}

.grid-info-num {
  font-size: 20px;
  font-weight: bold;
}

.grid-cont-right {
  flex: 1;
  text-align: center;
  font-size: 14px;
  color: #999;
}

.grid-num {
  font-size: 25px;
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
