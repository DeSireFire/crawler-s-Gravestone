<template>
	<div class="container">
    <div class="plugins-tips">日志详情</div>
    <div class="handle-row">
      <el-button :icon="Back" type="primary" @click="router.go(-1)">
        后退
      </el-button>
      <el-button :icon="Expand" type="primary" @click="goToParentPage('/projects_tabs')">
        相关项目
      </el-button>
      <el-button v-if="logTextarea.length !== 0" type="primary" :icon="RefreshRight" @click="handleLogContent">
        刷新日志
      </el-button>
      <el-button v-if="logTextarea.length !== 0" type="primary" :icon="Download" @click="downloadLog">
        下载日志
      </el-button>
    </div>
    <br/>
    <el-collapse v-model="activeNames" @change="handleChange">
      <el-collapse-item title="日志信息" name="1">
        <el-row>
          <el-col :span="11">
            <div>
              <el-form ref="formRef" :model="logInfo" label-width="80px">
                <el-form-item label="任务编号" prop="jid">
                  <el-input v-model="logInfo.jid" :disabled="true"></el-input>
                </el-form-item>
                <el-form-item label="任务名称" prop="name">
                  <el-input v-model="logInfo.name" :disabled="true"></el-input>
                </el-form-item>
              </el-form>
            </div>
          </el-col>
          <el-col :span="1"></el-col>
          <el-col :span="11">
            <div>
              <el-form ref="formRef" :model="logInfo" label-width="80px">
                <el-form-item label="所属项目" prop="p_nickname">
                  <el-input v-model="logInfo.p_nickname" :disabled="true"></el-input>
                </el-form-item>
                <el-form-item label="执行用户" prop="run_user">
                  <el-input v-model="logInfo.run_user" :disabled="true"></el-input>
                </el-form-item>
              </el-form>
            </div>
            <!--      <el-table :data="state.unread" :show-header="false" style="width: 100%">-->
            <!--        <el-table-column>-->
            <!--          <template #default="scope">-->
            <!--            <span class="message-title">{{ scope.row.title }}</span>-->
            <!--          </template>-->
            <!--        </el-table-column>-->
            <!--        <el-table-column prop="date" width="180"></el-table-column>-->
            <!--        <el-table-column width="120">-->
            <!--          <template #default="scope">-->
            <!--            <el-button size="small" @click="handleRead(scope.$index)">标为已读</el-button>-->
            <!--          </template>-->
            <!--        </el-table-column>-->
            <!--      </el-table>-->
          </el-col>
          <el-col :span="1"></el-col>
        </el-row>
      </el-collapse-item>
      <el-collapse-item title="日志筛选器" name="2">
        <el-form label-width="100px">
          <el-form-item label="日志等级">
            <el-select v-model="lv" placeholder="日志等级" class="handle-select mr10">
              <el-option  v-for="(item, index) in level_name" :key="index+1" :label="item" :value="item" @click="handleLogContent"></el-option>
              <el-option key="" label="无" value="" @click="handleLogContent"></el-option>
            </el-select>
          </el-form-item>
        </el-form>
        <el-form label-width="100px">
          <el-form-item label="关键词">
            <el-input v-model="keyword" clearable class="handle-input mr10" placeholder="关键词"></el-input>
          </el-form-item>
        </el-form>
      </el-collapse-item>
    </el-collapse>
    <p style="line-height: 50px">
      <el-tag class="ml-2" >日志内容（共{{ logLines.length }}行）</el-tag>
      <el-tag class="ml-2" type="warning">由于网页的处理性能有限，仅展示最新的1000行日志，大型日志建议使用日志下载功能。</el-tag>
    </p>
    <el-scrollbar>
      <ul>
        <li v-if="logLines.length === 0">日志加载中...</li>
        <li v-for="(item, index) in logLines" :key="index">
          <span>{{ item }}</span>
        </li>
      </ul>
    </el-scrollbar>
	</div>
</template>

<script setup lang="ts" name="logging_detail">
import {computed, reactive, ref, watch, watchEffect} from 'vue';
import {useRoute} from "vue-router";
import { useRouter } from 'vue-router';
import {Delete, Edit, Search, FullScreen, Close, RefreshRight, Download, Back, Expand} from '@element-plus/icons-vue';
import {downLoadLog, getLogContent} from "~/api/projects";
interface TableItem {
  id: string;
  wid: string;
  pid: string;
  jid: string;
  p_nickname: string;
  w_nickname: string;
  name: string;
  status: string;
  run_user: string;
  log_file_path: string;
  log_lv_warning: string;
  log_lv_error: string;
  log_lv_info: string;
  log_lv_debug: string;
  items_count: string;
  extra: string;
  create_time: string;
  end_time: string;
}

// 获取路由对象
const route = useRoute();
const router = useRouter();
// 返回父级页面的名称
const back = ref(route.query.back||'');
// 定义返回到父级页面的方法
const goToParentPage = (back_path?: string) => {
  back_path = back_path || ""; // 默认为空字符串
  console.log("back_path1:",back_path)
  if (!back_path) {
    back_path = back.value as string || ""
  }
  console.log("back_path2:",back_path)
  if ("/jobObjs" === back_path) {
    // 使用 $router.push() 导航到父级页面
    router.push({
      path: back_path,
    });
  } else if ("/projects_tabs" === back_path) {
    router.push({
      path: back_path,
      query: route.query,
    });
  } else {
    router.go(-1)
  }
};

const pid = ref(route.query.pid||'');
const wid = ref(route.query.wid||'');
const jid = ref(route.query.jid||'');
const lv = ref('');

const level_name = ref([
    "INFO",
    "WARNING",
    "ERROR",
    "DEBUG",
]);
// let params_info = {};
const handleProjectInfo = () => {
  const urlParams = new URLSearchParams(window.location.hash.split('?')[1]);
  pid.value = urlParams.get('pid') as string;
  wid.value = urlParams.get('wid') as string;
  jid.value = urlParams.get('jid') as string;
  back.value = urlParams.get('back') as string;
  // params_info = Object.fromEntries(urlParams.entries());
};
// el-collapse 下拉展开的编号
const activeNames = ref(['1'])
const handleChange = (val: string[]) => {
  console.log("handleChange,val", val)
}
const keyword = ref('');
const logLines = computed(() => {
	return logArray.value.filter(item => {
		return item.indexOf(keyword.value) !== -1;
	});
});

// 使用 ref 来保存参数信息
const logExists = ref(false);
// 监听路由参数的变化
watch(() => route.query, (newPid, oldPid) => {
  // 如果跳出日志详情页面，则不再执行往后的内容
  const currentPath = route.path;
  logExists.value = '/logging_detail' === currentPath;
  if (logExists.value) {
    handleProjectInfo();
    handleLogContent();
  }
});


// 获取日志文件内容
// 日志文本容器
let logMointForm = reactive({
  pid: "",
  wid: "",
  jid: "",
  lv: "",
})
const logInfo = reactive({
  jid: "",
  name: "",
  w_nickname: "",
  p_nickname: "",
  run_user: "",
})
const logTextarea = ref('')
// 保存当前日志到文件
function saveLog() {
  const date = new Date().toISOString().slice(0, 10);
  const filename = `日志导出-${logInfo.name}-${logInfo.jid}-${date}.log`;
  const blob = new Blob([logTextarea.value + '\n' + date + "时导出日志..."], { type: 'text/plain' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = filename;
  link.click();
}

// 下载全文日志文件
const downloadLog = async () => {
  let watiGetInfo:any = logMointForm;
  try {
    const response = (await downLoadLog(watiGetInfo))
    const date = new Date().toISOString().slice(0, 10);
    const filename = `日志导出-${logInfo.name}-${logInfo.jid}-${date}.log`;
    console.log("response--->",response)
    const blob = new Blob([response.data.content + '\n' + date + "时导出日志..."], { type: 'application/octet-stream' });

    // 写法一
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = filename;
    link.click();
    // 写法二
    // const url = window.URL.createObjectURL(blob);
    // const a = document.createElement('a');
    // a.href = url;
    // a.download = filename; // 可以根据你的需求设置文件名
    // a.click();
    // window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error('下载日志文件失败', error);
  }
}

const logArray = ref<Array<string>>([]);
const handleLogContent = async () => {
  handleProjectInfo();
  logMointForm.pid = pid.value as string;
  logMointForm.wid = wid.value as string;
  logMointForm.jid = jid.value as string;
  logMointForm.lv = lv.value;
  let watiGetInfo:any = logMointForm;
  // 获取日志内容
  const response = (await getLogContent(watiGetInfo))
  logTextarea.value = response.data.content
  logInfo.jid = jid.value as string
  logInfo.name = response.data.name
  logInfo.w_nickname = response.data.w_nickname
  logInfo.p_nickname = response.data.p_nickname
  logInfo.run_user = response.data.run_user

  // Split the logTextarea data into an array of lines
  logArray.value = logTextarea.value.split('\n');
}
handleLogContent();

</script>

<style scoped>
.handle-row {
  margin-top: 30px;
}

.el-scrollbar__wrap {
  overflow: auto;
  height: 100%;
  background-color: #f5f5f5;
  border-radius: 4px;
  height: 400px;
  border: 1px solid #ccc;
}

.handle-box {
  margin-bottom: 20px;
}

.handle-select {
  width: 120px;
}

.handle-input {
  width: 300px;
}

.example-p {
	height: 45px;
	display: flex;
	align-items: center;
}
/*.search-box {*/
/*	text-align: center;*/
/*	margin-top: 10px;*/
/*}*/
/*.search {*/
/*	width: 300px;*/
/*}*/
ul, li {
	list-style: none;
}
</style>
