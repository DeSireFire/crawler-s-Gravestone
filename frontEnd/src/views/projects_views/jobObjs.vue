<template>
  <div class="container">
    <div class="plugins-tips">
      <b>任务实例总表</b>
      <el-tooltip>
        <template #content>
          <p>“任务实例总表”</p>
          <p>是一个展示所有任务实例的列表，不区分项目和工作流。</p>
          <p>超出用户访问权限的部分任务实例将不会展示。</p>
          <p>默认根据记录开始时间排序。</p>
        </template>
        <el-icon><InfoFilled /></el-icon>
      </el-tooltip>
    </div>
    <div class="handle-box">
      <el-input v-model="query.keyword" placeholder="关键词搜索" class="handle-input mr10"></el-input>
<!--      <el-button type="primary" :icon="Search" @click="filteredData">搜索列表</el-button>-->
      <el-button type="primary" :icon="Refresh" @click="handleFlush()">刷新列表</el-button>
    </div>
    <el-scrollbar>
      <el-table
        :data="filteredData"
        :border="true"
        stripe
        class="table"
        ref="multipleTable"
        @sort-change="handleSortChange"
        :default-sort="{ prop: 'create_time', order: 'descending' }"
        header-cell-class-name="table-header"
      >
        <el-table-column prop="id" label="编号" width="55" align="center"></el-table-column>
        <el-table-column width="300" label="实例名称" :show-overflow-tooltip="true">
          <template #default="scope">
            {{ scope.row.name }}
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
        <el-table-column prop="p_nickname" width="200" label="所属项目" :show-overflow-tooltip="true"></el-table-column>
        <el-table-column prop="w_nickname" width="200" label="工作流" :show-overflow-tooltip="true"></el-table-column>

        <el-table-column class-name="log-num" width="50" label="错误" :show-overflow-tooltip="true">
          <template #default="scope"><span class="error-color">{{ scope.row.log_lv_error }}</span></template>
        </el-table-column>
        <el-table-column class-name="log-num" width="50" label="警告" :show-overflow-tooltip="true">
          <template #default="scope"><span class="warning-color">{{ scope.row.log_lv_warning }}</span></template>
        </el-table-column>
        <el-table-column class-name="log-num" width="50" label="常规" :show-overflow-tooltip="true">
          <template #default="scope"><span class="info-color">{{ scope.row.log_lv_info }}</span></template>
        </el-table-column>
        <el-table-column class-name="log-num" width="100" label="数据计数" :show-overflow-tooltip="true">
          <template #default="scope"><span class="ok-color">{{ scope.row.items_count }}</span></template>
        </el-table-column>

        <el-table-column width="100" label="执行用户" :show-overflow-tooltip="true">
          <template #default="scope">{{ scope.row.run_user }}</template>
        </el-table-column>
        <el-table-column width="140" label="记录开始时间" prop="create_time" sortable :sort-method="sortTime">
          <template #default="{ row }">{{ formatDate(row.create_time) }}</template>
        </el-table-column>
        <el-table-column width="140" label="记录结束时间" prop="end_time" sortable :sort-method="sortTime">
          <template #default="{ row }">{{ formatDate(row.end_time) }}</template>
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
  </div>
</template>

<script setup lang="ts" name="sub_jobObj">
import { ref, reactive, computed } from 'vue';
import { useRoute } from 'vue-router';
import { ElMessage, ElMessageBox } from 'element-plus';
import {getJobs, delJobs, getLogContent, getProjectsNames} from '~/api/projects';
// import { um_api } from "~/store/user_mange";
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
// 获取路由对象
const route = useRoute();
const query = reactive({
  filterWord: '',
  keyword: '',
  pageIndex: 1,
  pageSize: 10,
  log_projects: [],
});
const tableData = ref<TableItem[]>([]);
const pageTotal = ref(0);
const filter = reactive({})
// 刷新数据
const handleFlush = async (init = true) => {
  // 获取数据
  const res = (await getJobs({}))

  if (res.data.pageTotal == 0) {
    ElMessage.warning(`未查询到任务实例！`);
  }
  // 是否初始化
  if (init && res.data.pageTotal !== 0) {
    // 载入数据
    tableData.value = res.data.list.slice(0, query.pageSize);
    pageTotal.value = res.data.pageTotal || 1;
    // 缓存数据
    localStorage.setItem('jobs_list', JSON.stringify(res.data));
  }
};
// 打开页面就刷新
handleFlush();

// 计算属性，根据搜索关键字筛选数据
const filteredData = computed(() => {
  if (!query.keyword) {
    return tableData.value;
  }

  const keyword = query.keyword;
  console.log("query", query)
  return   tableData.value.filter(item =>
      item.name.toLowerCase().includes(keyword) || String(item.p_nickname).includes(keyword)
  );
});

// 排序相关
const sortKey = ref('create_time');
const sortOrder = ref('descending');

const sortTime = (a: string, b: string) => {
  const dateA = new Date(a);
  const dateB = new Date(b);
  const order = sortOrder.value as 'ascending' | 'descending'; // 明确类型
  if (order === 'ascending') {
    return dateA.getTime() - dateB.getTime();
  } else {
    return dateB.getTime() - dateA.getTime();
  }
};


const handleSortChange = ({ column, prop, order }: any) => {
  sortKey.value = prop;
  sortOrder.value = order;
};

// 定义 formatDate 函数
const formatDate = (time: string) => {
  const date = new Date(time);
  return date.toLocaleString(); // 根据需要格式化时间显示
};

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
          const sub_flush = (await getJobs({}))
          console.log("sub_flush", sub_flush)
          localStorage.setItem('jobs_list', JSON.stringify(sub_flush.data));
          let temp = tableData.value.splice(index, 1)[0];
          tableData.value = sub_flush.data.list
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
</script>

<style scoped>
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

