<!-- sub_workerLinks.vue -->
<template>
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
</template>

<script setup lang="ts" name="sub_projectDetail">
import { ref, reactive } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { getProject } from '~/api/projects';
import { um_api } from "~/store/user_mange";
import { Delete, Edit, Plus,Refresh } from '@element-plus/icons-vue';
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
});
const query = um_api.query
const pageTotal = ref(0);
const pid = ref('');
let params_info = {
  id: "",
  pid: "",
  name: "",
  nickname: "",
  description: "",
  author: "",
  create_time: "",
  update_time: "",
};
const handleProjectInfo = () => {
  const urlParams = new URLSearchParams(window.location.hash.split('?')[1]);
  pid.value = urlParams.get('pid') as string;
};
handleProjectInfo();

// 刷新数据
const handleFlush = async (init = true) => {
  // 获取pid
  handleProjectInfo();

  if (pid.value != '') {
    // 获取数据
    const res = (await getProject({
      pid: pid.value
    }))

    params_info.id = res.data.id
    params_info.pid = res.data.pid
    params_info.name = res.data.name
    params_info.nickname = res.data.nickname
    params_info.description = res.data.description
    params_info.author = res.data.author
    params_info.create_time = res.data.create_time
    params_info.update_time = res.data.update_time

  } else {
    ElMessage.error(`未找到项目ID，无法获取项目相关工作流信息！`);
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

