<!-- sub_workerLinks.vue -->
<template v-if="ptabs === 'second'">
  <div class="plugins-tips">任务实例</div>
  <div class="handle-box">
    <el-button type="primary" :icon="Refresh" @click="handleFlush()">刷新</el-button>
  </div>
  <el-scrollbar>
    <el-table :data="tableData" border class="table" ref="multipleTable" header-cell-class-name="table-header">
      <el-table-column prop="id" label="编号" width="55" align="center"></el-table-column>
      <el-table-column label="实例名称">
        <template #default="scope">
          <a href="javascript:void(0);" @click="handleUpToken(scope.$index, scope.row)">{{ scope.row.name }}</a>
        </template>
      </el-table-column>
      <el-table-column prop="status" width="100" label="状态" align="center">
        <template #default="scope">
          <el-tag
              :type="['warning', 'success', 'info', 'error', 'danger'][scope.row.status]"
          >
            {{ ['未知', '执行中', '结束', '中断', '失败'][scope.row.status] }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="log_lv_error" width="50" label="错误"></el-table-column>
      <el-table-column prop="log_lv_warning" width="50" label="警告"></el-table-column>
      <el-table-column prop="log_lv_info" width="50" label="常规"></el-table-column>
      <el-table-column prop="items_count" width="100" label="数据计数"></el-table-column>
      <el-table-column width="100" label="执行用户">
        <template #default="scope">{{ scope.row.run_user }}</template>
      </el-table-column>
      <el-table-column width="160" label="记录开始时间">
        <template #default="scope">{{ scope.row.create_time }}</template>
      </el-table-column>
      <el-table-column width="160" label="记录结束时间">
        <template #default="scope">{{ scope.row.end_time }}</template>
      </el-table-column>
      <el-table-column label="操作" width="300" align="center" fixed="right">
        <template #default="scope">
          <el-button text :icon="Edit" @click="handleMonit(scope.$index, scope.row)" v-permiss="15">
            日志预览
          </el-button>
          <el-button text :icon="Edit"
           @click="$router.push({
           path: '/logging_detail',
           query: {
             pid: scope.row.pid,
             wid: scope.row.wid,
             jid: scope.row.jid,
           }
           })"
           v-permiss="15">
            日志
          </el-button>

          <el-button text :icon="Delete" class="red" @click="handleDelete(scope.$index, scope.row)" v-permiss="16">
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-scrollbar>

  <!-- 日志查看弹出框 -->
  <el-dialog
      v-model="logVisible"
      title="查看日志"
      width="50%"
      :fullscreen="fullscreen"
      :before-close="handleClose"
      :show-close="false"
      :close-on-click-modal="false"
      destroy-on-close
  >
    <!-- 弹窗头部 -->
    <template #header="{ close, titleId, titleClass, scope }">
      <div class="my-header">
        <h4 :id="titleId" :class="titleClass">查看日志</h4>
        <div class="dialog-header-right">
          <el-button link :icon="RefreshRight" @click="handleLogContent"></el-button>
          <el-button link :icon="FullScreen" @click="changeScreen"></el-button>
          <el-button link :icon="Close" @click="close"></el-button>
        </div>
      </div>
    </template>

    <el-input
        v-model="logTextarea"
        :autosize="{ minRows: 10, maxRows: 20 }"
        :readonly="false"
        type="textarea"
        placeholder="日志加载中..."
        class="log-text"
    />

    <template #footer>
      <span class="dialog-footer">
        <el-button type="primary" @click="fullscreen = false; logVisible = false;">
          关闭
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup lang="ts" name="sub_jobObj">
import { ref, reactive } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import {getJobs, delJobs, getLogContent} from '~/api/projects';
import { um_api } from "~/store/user_mange";
import {Delete, Edit, Search, Plus, FullScreen, Close, RefreshRight, Refresh} from '@element-plus/icons-vue';
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

const query = um_api.query
const tableData = ref<TableItem[]>([]);
const pageTotal = ref(0);
const pid = ref('');
let params_info = {};
const handleProjectInfo = () => {
  const urlParams = new URLSearchParams(window.location.hash.split('?')[1]);
  pid.value = urlParams.get('pid') as string;
  params_info = Object.fromEntries(urlParams.entries());
};
handleProjectInfo();

// 刷新数据
const handleFlush = async (init = true) => {
  // 获取pid
  handleProjectInfo();

  if (pid.value != '') {
    // 获取数据
    const res = (await getJobs({
      pid: pid.value
    }))

    if (res.data.pageTotal == 0) {
      ElMessage.warning(`该项目没有定义工作流，无法获取有关信息！`);
    }

    // 是否初始化
    if (init && res.data.pageTotal !== 0) {
      // 载入数据
      tableData.value = res.data.list.slice(0, query.pageSize);
      pageTotal.value = res.data.pageTotal || 1;
      // 缓存数据
      // localStorage.setItem('jobs_list', JSON.stringify(res.data));
    }
  } else {
    ElMessage.error(`未找到项目ID，无法获取项目相关工作流信息！`);
  }
};
// 打开页面就刷新
handleFlush();

// 删除操作
let delform = reactive({
  pid: '',
  wid: '',
  jid: '',
});
const handleDelete = (index: number, row: any) => {
  // 二次确认删除
  ElMessageBox.confirm('确定要删除吗？', '提示', {
    type: 'warning'
  })
      .then(async () => { /* 处理正常时 */
        // 获取当前表行数据
        delform.wid = row.wid;
        delform.pid = row.pid;
        delform.jid = row.jid;
        // 向后端发起删除操作
        const response = (await delJobs(delform));
        if (response.isSuccess) {
          // 响应删除成功则弹出提示
          ElMessage.success('删除成功！');
          // 刷新缓存数据
          const sub_flush = (await getJobs({
            pid: pid.value
          }))
          localStorage.setItem('jobs_list', JSON.stringify(sub_flush.data));
          let temp = tableData.value.splice(index, 1)[0];
          pageTotal.value -= 1

        } else {
          // 响应删除失败则弹出错误
          throw new Error(response.errMsg);
        }
      })
      .catch((error) => { /* 处理失败时 */
        ElMessage.error(`删除失败! ${error}`);
      });
};

// 定位待处理行的下标
let idx: number = -1;
// 日志内容查看
// 日志窗口的显示开关
const logVisible = ref(false)
// 日志窗口待操作的变量
let logMointForm = reactive({
  pid: '',
  wid: '',
  jid: '',
})

// 日志窗口处理器（void类型表示函数没有返回值）
const handleMonit = (index: number, row: any, done: () => void) => {
  idx = index;
  logMointForm.pid = row.pid;
  logMointForm.wid = row.wid;
  logMointForm.jid = row.jid;
  logVisible.value = true;
  // 获取日志文本
  handleLogContent(index,row)
  // console.log("handleMonit~")
};

//全屏
const fullscreen = ref(false)

let minRows = ref(10)
let maxRows = ref(20)
// let textArea = {
//   "minRows":minRows,
//   "maxRows":maxRows,
// }
const changeScreen = () => {
  if (fullscreen.value == true) {
    fullscreen.value = false;
    minRows.value = 10
    maxRows.value = 20
    console.log("textAreaRows true", minRows, maxRows)
  } else {
    fullscreen.value = true;
    minRows.value = 50
    maxRows.value = 100
    console.log("textAreaRows false", minRows, maxRows)
  }
  //fullscreen.value = !fullscreen.value;
}

// 弹窗关闭确认
const handleClose = (done: () => void) => {
  // 弹窗关闭确认，:before用法的实践
  ElMessageBox.confirm('确定要退出日志查看吗?')
      .then(() => {
        done()
        changeScreen()
      })
      .catch(() => {
        // catch error
      })
}

// 获取日志文件内容
// 日志文本容器
const logTextarea = ref('')
const handleLogContent = async (index: number, row: any) => {
  let watiGetInfo: TableItem = row ?? logMointForm;
  // console.log("row", row)
  // console.log("watiGetInfo", watiGetInfo)
  const response = (await getLogContent(watiGetInfo))
  logTextarea.value = response.data.content
}

</script>

<style scoped>
.my-header {
  display: flex;
  flex-direction: row;
  justify-content: space-between;

  align-items: center;
}

.dialog-header-right {
  display: flex;
}

.dialog-header-right i {
  margin-left: 10px;
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
.table {
  width: 100%;
  font-size: 12px;
}
.red {
  color: #F56C6C;
}
.mr10 {
  margin-right: 10px;
}
.table-td-thumb {
  display: block;
  margin: auto;
  width: 40px;
  height: 40px;
}
</style>

