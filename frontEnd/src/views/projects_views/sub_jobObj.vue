<!-- sub_workerLinks.vue -->
<template v-if="ptabs === 'second'">
  <div class="plugins-tips">任务实例</div>
  <div class="handle-box">
    <el-button type="primary" :icon="Refresh" @click="handleFlush()">刷新</el-button>
  </div>
  <el-table :data="tableData" border class="table" ref="multipleTable" header-cell-class-name="table-header">
    <el-table-column prop="id" label="编号" width="55" align="center"></el-table-column>
    <el-table-column label="实例名称">
      <template #default="scope">
        <a href="javascript:void(0);" @click="handleUpToken(scope.$index, scope.row)">{{ scope.row.name }}</a>
    </template>
    </el-table-column>
    <el-table-column prop="status" width="70" label="状态">
      <template #default="scope">
        <el-tag
            :type="['warning', 'info', 'success', 'error', 'danger'][scope.row.status]"
        >
          {{ ['未知', '执行中', '结束', '中断', '失败'][scope.row.status] }}
        </el-tag>
      </template>
    </el-table-column>
    <el-table-column prop="log_lv_error" width="50" label="错误"></el-table-column>
    <el-table-column prop="log_lv_warning" width="50" label="警告"></el-table-column>
    <el-table-column prop="log_lv_info" width="50" label="常规"></el-table-column>
    <el-table-column width="100" label="执行用户">
      <template #default="scope">{{ scope.row.run_user }}</template>
    </el-table-column>
    <el-table-column width="160" label="记录开始时间">
      <template #default="scope">{{ scope.row.create_time }}</template>
    </el-table-column>
    <el-table-column width="160" label="记录结束时间">
      <template #default="scope">{{ scope.row.end_time }}</template>
    </el-table-column>
    <el-table-column label="操作" width="300" align="center">
      <template #default="scope">
        <el-button text :icon="Edit" @click="handleEdit(scope.$index, scope.row)" v-permiss="15">
          编辑
        </el-button>
        <el-button text :icon="Delete" class="red" @click="handleDelete(scope.$index, scope.row)" v-permiss="16">
          删除
        </el-button>
      </template>
    </el-table-column>
  </el-table>
</template>

<script setup lang="ts" name="sub_jobObj">
import { ref, reactive } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { getJobs, delJobs } from '~/api/projects';
import { um_api } from "~/store/user_mange";

import { Delete, Edit, Plus,Refresh } from '@element-plus/icons-vue';
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
  // 获取数据
  const res = (await getJobs({
    pid: pid.value
  }))
  // 是否初始化
  if (init) {
    // 载入数据
    tableData.value = res.data.list.slice(0, query.pageSize);
    pageTotal.value = res.data.pageTotal || 1;
    // 缓存数据
    localStorage.setItem('jobs_list', JSON.stringify(res.data));
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
          const sub_flush = (await getJobs())
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
</style>

