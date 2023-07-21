<!-- sub_workerLinks.vue -->
<template v-if="message === 'second'">
  <div class="plugins-tips">工作流定义</div>
  <div class="handle-box">
    <el-button type="primary" :icon="Plus" @click="handleAdd()">创建工作流</el-button>
  </div>
  <el-table :data="tableData" border class="table" ref="multipleTable" header-cell-class-name="table-header">
    <el-table-column prop="id" label="编号" width="55" align="center"></el-table-column>
    <el-table-column label="项目名称">
      <template #default="scope"><a href="#/workers_info">{{ scope.row.nickname }}</a></template>
    </el-table-column>
    <el-table-column width="100" label="工作流名称">
      <template #default="scope">--</template>
    </el-table-column>
    <el-table-column width="100" label="所属用户">
      <template #default="scope">{{ scope.row.author }}</template>
    </el-table-column>
    <el-table-column prop="description" width="300" label="背景描述" :show-overflow-tooltip="true">
    </el-table-column>
    <el-table-column width="200" label="创建时间">
      <template #default="scope">{{ scope.row.create_time }}</template>
    </el-table-column>
    <el-table-column label="操作" width="200" align="center">
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

<script setup lang="ts" name="sub_workerLinks">
import { ref, reactive } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import {getWorkers, addProjects, delProjects, updateProjects} from '~/api/projects';
import { um_api } from "~/store/user_mange";
import { Delete, Edit, Plus,Refresh } from '@element-plus/icons-vue';
interface TableItem {
  id: number;
  wid: string;
  pid: string;
  p_nickname: string;
  name: string;
  description: string;
  status: string;
  modify_user: string;
  extra: string;
  create_time: string;
  update_time: string;
}

const query = um_api.query
const tableData = ref<TableItem[]>([]);
const pageTotal = ref(0);
// 刷新数据
const handleFlush = async (init = true) => {
  // 获取数据
  const res = (await getWorkers())
  // 是否初始化
  if (init) {
    // 载入数据
    tableData.value = res.data.list.slice(0, query.pageSize);
    pageTotal.value = res.data.pageTotal || 1;
    // 缓存数据
    localStorage.setItem('workers_list', JSON.stringify(res.data));
  }
};
// 打开页面就刷新
handleFlush();



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
  font-size: 14px;
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

