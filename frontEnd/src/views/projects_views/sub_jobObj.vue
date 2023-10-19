<!-- sub_workerLinks.vue -->
<template v-if="ptabs === 'second'">
  <div class="plugins-tips">
    <b>任务实例</b>:
    <el-tag class="ml-2" type="success">{{ project_info.name }}</el-tag>
  </div>
  <div class="handle-box">
    <el-button type="primary" :icon="Refresh" @click="handleFlush()">刷新</el-button>
  </div>
  <el-scrollbar>
    <el-table :data="tableResData" border class="table" ref="multipleTable" header-cell-class-name="table-header" max-height="480">
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
            {{ ['未知', '执行中', '结束', '中断', '错误'][scope.row.status] }}
          </el-tag>
        </template>
      </el-table-column>

      <el-table-column class-name="log-num" width="100" label="错误" :show-overflow-tooltip="true">
        <template #default="scope"><span class="error-color">{{ scope.row.log_lv_error }}</span></template>
      </el-table-column>
      <el-table-column class-name="log-num" width="100" label="警告" :show-overflow-tooltip="true">
        <template #default="scope"><span class="warning-color">{{ scope.row.log_lv_warning }}</span></template>
      </el-table-column>
      <el-table-column class-name="log-num" width="100" label="常规" :show-overflow-tooltip="true">
        <template #default="scope"><span class="info-color">{{ scope.row.log_lv_info }}</span></template>
      </el-table-column>
      <el-table-column class-name="log-num" width="200" label="数据计数" :show-overflow-tooltip="true">
        <template #default="scope"><span class="ok-color">{{ scope.row.items_count }}</span></template>
      </el-table-column>

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
          <el-button text :icon="Edit"
           @click="$router.push({
           path: '/logging_detail',
           query: {
             pid: scope.row.pid,
             wid: scope.row.wid,
             jid: scope.row.jid,
             title: scope.row.name,
             back: route.path,
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
  <!-- 分页组件 -->
  <div class="pagination">
    <el-pagination
        background
        layout="total, sizes, prev, pager, next, jumper"
        v-model="query.pageIndex"
        v-model:page-size="query.pageSize"
        :page-sizes="[10, 20, 30, 40, 50, 100]"
        :pager-count="5"
        :page-size="query.pageSize"
        :total="pageTotal"
        @size-change="handleSizeChange"
        @current-change="handlePageChange"
    />
  </div>
</template>

<script setup lang="ts" name="sub_jobObj">
import {ref, reactive, watch} from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import {getJobs, delJobs, getLogContent} from '~/api/projects';
import {useRoute} from "vue-router";
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
// 加载状态
const table_loading = ref(true);
// 声明 props
const props = defineProps<{
  pid: String,
  pname: String,
}>();
const pid = ref(props.pid||'');
const query = reactive({
  filterKey: '',
  filterValue: '',
  keyword: '',
  pageIndex: 1,
  pageSize: 10
});
// const tableData = ref<TableItem[]>([]);
// 表格整合数据
const tableResData = ref<TableItem[]>([]);

const pageTotal = ref(0);
let project_info = reactive({
  pid: '',
  name: '',
});
// const handleProjectInfo = () => {
//   const urlParams = new URLSearchParams(window.location.hash.split('?')[1]);
//   pid.value = urlParams.get('pid') as string;
//   project_info.pid = urlParams.get('pid') as string;
//   project_info.name = urlParams.get('name') as string;
// };
// handleProjectInfo();

// 刷新数据
const handleFlush = async (init = true) => {
  if (!table_loading.value) {
    table_loading.value = true;
  }

  // 获取pid
  pid.value = props.pid
  project_info.name = props.pname as string ||''

  if (pid.value != '') {
    // 获取数据
    const res = (await getJobs({
      pid: pid.value
    }))

    if (res.data.pageTotal == 0) {
      ElMessage.warning(`该项目没有任务实例，无法获取有关信息！`);
      tableResData.value = [];
    }

    // 是否初始化
    if (init && res.data.pageTotal !== 0) {
      // 载入数据
      tableResData.value = res.data.list.slice(0, query.pageSize);
      pageTotal.value = res.data.pageTotal || 1;
      // 清空筛选器
      query.filterKey = '';
      query.filterValue = '';
      query.keyword = '';

      // 缓存数据
      localStorage.setItem('sub_jobs_list', JSON.stringify(res.data));
    }
  } else {
    ElMessage.error(`未找到项目ID，无法获取项目相关工作流信息！`);
  }
  table_loading.value = false;
};
// 打开页面就刷新
handleFlush();

const route = useRoute();
// 监听路由参数的变化
watch(() => props.pid, (newPid, oldPid) => {
  pid.value = newPid;
  handleFlush();
});

// todo 通过日志详情页返回时会携带jid,似乎可以增加额外的处理。
// const jid = ref(route.query.jid||'');


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
          // 刷新缓存数据
          const sub_flush = (await getJobs({
            pid: pid.value
          }))
          localStorage.setItem('sub_jobs_list', JSON.stringify(sub_flush.data));
          let temp = tableResData.value.splice(index, 1)[0];
          pageTotal.value -= 1
          // 响应删除成功则弹出提示
          ElMessage.success('删除成功！');
        } else {
          // 响应删除失败则弹出错误
          // throw new Error(response.errMsg);
          ElMessage.error(`业务处理时发生错误! ${response.errMsg}`);
        }
      })
      .catch((error) => { /* 处理失败时 */
        ElMessage.error(`删除失败! ${error}`);
      });
};

// 渲染数据处理
// 声明 jobsList 和 keyword 的类型
let jobsList: { list: TableItem[] };
const handleResTable = () => {
  // 初始化中间变量
  let temp:TableItem[] = [];

  // 数据来源：后台获取、缓存读取
  // 从localStorage中获取缓存数据
  jobsList = JSON.parse(localStorage.getItem('sub_jobs_list') as string);

  // 如果缓存数据不存在，运行handleFlush函数并重新获取
  if (!jobsList) {
    handleFlush();
    jobsList = JSON.parse(localStorage.getItem('sub_jobs_list') as string);
  }
  temp = jobsList.list;

  if (query.pageIndex >= 1) {
    let cursor_start = (query.pageIndex - 1) * query.pageSize
    let cursor_end = cursor_start + query.pageSize
    temp = temp.slice(cursor_start, cursor_end);
  } else {
    temp = temp.slice(0, query.pageSize);
  }
  tableResData.value = temp;
};

// 分页操作
const handlePageChange = (pageNumber: number) => {
  query.pageIndex = pageNumber
  handleResTable()
};
const handleSizeChange = (pageSize: number) => {
  query.pageSize = pageSize
  handleResTable()
};

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

.log-num span {
  font-size: 20px;
  font-weight: bold;
}

.log-num .error-color {
  color: rgb(245, 108, 108);
}

.log-num .warning-color {
  color: #e6a23c;
}

.log-num .info-color {
  color: #409eff;
}

.log-num .ok-color {
  color: rgb(99, 214, 211);
}
</style>

