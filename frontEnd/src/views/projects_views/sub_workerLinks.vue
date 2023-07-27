<!-- sub_workerLinks.vue -->
<template v-if="ptabs === 'second'">
  <div class="plugins-tips">工作流定义</div>
  <div class="handle-box">
    <el-button type="primary" :icon="Plus" @click="handleAdd()">创建工作流</el-button>
    <el-button type="primary" :icon="Refresh" @click="handleFlush()">刷新</el-button>
  </div>

  <el-scrollbar>
    <el-table :data="tableData" border class="table" ref="multipleTable" header-cell-class-name="table-header">
      <el-table-column prop="id" label="编号" width="55" align="center"></el-table-column>
      <el-table-column label="工作流名称">
        <template #default="scope">
          <a href="javascript:void(0);" @click="handleUpToken(scope.$index, scope.row)">{{ scope.row.name }}</a>
        </template>
      </el-table-column>
      <el-table-column width="100" label="修改用户">
        <template #default="scope">{{ scope.row.modify_user }}</template>
      </el-table-column>
      <el-table-column width="100" label="所属项目" :show-overflow-tooltip="true">
        <template #default="scope">{{ scope.row.p_nickname }}</template>
      </el-table-column>
      <el-table-column width="100" label="采集频率">
        <template #default="scope">{{ scope.row.crawl_frequency }}</template>
      </el-table-column>
      <el-table-column prop="description" width="300" label="背景描述" :show-overflow-tooltip="true">
      </el-table-column>
      <el-table-column width="160" label="创建时间">
        <template #default="scope">{{ scope.row.create_time }}</template>
      </el-table-column>
      <el-table-column label="操作" width="300" align="center" fixed="right">
        <template #default="scope">
          <el-button text :icon="Edit" @click="handleUpToken(scope.$index, scope.row)" v-permiss="15">
            密钥
          </el-button>
          <el-button text :icon="Edit" @click="handleEdit(scope.$index, scope.row)" v-permiss="15">
            编辑
          </el-button>
          <el-button text :icon="Delete" class="red" @click="handleDelete(scope.$index, scope.row)" v-permiss="16">
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-scrollbar>

  <!-- 弹出框 -->
  <el-dialog title="创建项目" v-model="addVisible" width="40%">
    <el-form label-width="100px">
      <el-form-item label="工作流名称">
        <el-input v-model="addForm.name"></el-input>
      </el-form-item>
      <el-form-item label="预计采集频率">
        <el-select v-model="addForm.crawl_frequency" placeholder="采集频率" class="handle-select mr10">
          <el-option key="0" label="周更" value="周更"></el-option>
          <el-option key="1" label="月更" value="月更"></el-option>
          <el-option key="2" label="季更" value="季更"></el-option>
          <el-option key="3" label="年更" value="年更"></el-option>
          <el-option key="4" label="临时" value="临时"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="背景描述">
        <el-input
            type="textarea" v-model="addForm.description"
            placeholder="描述采集背景，采集内容，采集来源等..."
        ></el-input>
      </el-form-item>
    </el-form>
    <template #footer>
				<span class="dialog-footer">
					<el-button @click="addVisible = false">取 消</el-button>
					<el-button type="primary" @click="addSaveEdit">确 定</el-button>
				</span>
    </template>
  </el-dialog>

  <el-dialog title="编辑项目" v-model="editVisible" width="30%">
    <el-form label-width="100px">
      <el-form-item label="工作流名称">
        <el-input v-model="editForm.nickname" :placeholder="editForm.nickname"></el-input>
      </el-form-item>
      <el-form-item label="预计采集频率">
        <el-select v-model="editForm.crawl_frequency" placeholder="采集频率" class="handle-select mr10">
          <el-option key="0" label="周更" value="周更"></el-option>
          <el-option key="1" label="月更" value="月更"></el-option>
          <el-option key="2" label="季更" value="季更"></el-option>
          <el-option key="3" label="年更" value="年更"></el-option>
          <el-option key="4" label="临时" value="临时"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="背景描述">
        <el-input
            type="textarea" v-model="editForm.description"
            placeholder="描述采集背景，采集内容，采集来源等..."
        ></el-input>
      </el-form-item>
    </el-form>
    <template #footer>
				<span class="dialog-footer">
					<el-button @click="editVisible = false">取 消</el-button>
					<el-button type="primary" @click="editSaveEdit">确 定</el-button>
				</span>
    </template>
  </el-dialog>

  <el-dialog title="信息收集密钥" v-model="upTokenVisible" width="30%">
    <el-row>
      <el-col :span="24">
        <div class="plugins-tips">将密钥作为参数填入信息上传工具中即可。</div>
      </el-col>
    </el-row>
    <br>
    <el-row>
      <el-col :span="24">
        <el-form label-width="100px">
          <el-form-item label="工作流名称">
            <el-input v-model="upTokenForm.nickname"></el-input>
          </el-form-item>
        </el-form>
        <el-form label-width="100px">
          <el-form-item label="上传密钥">
            <el-input v-model="upTokenForm.wid"></el-input>
          </el-form-item>
        </el-form>
        <el-form label-width="100px">
          <el-form-item label="原始流名称">
            <el-input v-model="upTokenForm.name"></el-input>
          </el-form-item>
        </el-form>
      </el-col>
    </el-row>
    <template #footer>
				<span class="dialog-footer">
					<el-button @click="upTokenVisible = false">关 闭</el-button>
				</span>
    </template>
  </el-dialog>
</template>

<script setup lang="ts" name="sub_workerLinks">
import {ref, reactive, onBeforeUpdate, watch, onMounted} from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import {getWorkers, addWorkers, delWorkers, updateWorkers } from '~/api/projects';
import { um_api } from "~/store/user_mange";
import { Delete, Edit, Plus,Refresh } from '@element-plus/icons-vue';
// watch(
//     a,
//     () => {
//
// })

interface TableItem {
  id: number;
  wid: string;
  pid: string;
  p_nickname: string;
  name: string;
  nickname: string;
  crawl_frequency: string;
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
    const res = (await getWorkers({
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
      // localStorage.setItem('workers_list', JSON.stringify(res.data));
    }
  } else {
    ElMessage.error(`未找到项目ID，无法获取项目相关工作流信息！`);
  }
};
// 打开页面就刷新
handleFlush();

// 增删改
// 新增操作，表格新增项目时弹窗和保存
const addVisible = ref(false);
let addForm = reactive({
  name: '',
  pid: pid.value,
  modify_user: '',
  crawl_frequency: '',
  description: '',
});
const handleAdd = () => {
  addVisible.value = true;
};
const addSaveEdit = async () => {
  addForm.modify_user = localStorage.getItem('ms_username') as string;
  // 向后端发起操作
  const response = (await addWorkers(addForm));
  if (response.isSuccess) {
    addVisible.value = false;
    handleFlush();
    ElMessage.success(`新增 ${addForm.name} 成功！`);
  } else {
    ElMessage.error(`新增 ${addForm.name} 失败！`);
  }
};

// 删除操作
let delform = reactive({
  pid: '',
  wid: '',
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
        // 向后端发起删除操作
        const response = (await delWorkers(delform));
        if (response.isSuccess) {
          // 响应删除成功则弹出提示
          ElMessage.success('删除成功！');
          // 刷新缓存数据
          const sub_flush = (await getWorkers({
            pid:pid.value
          }))
          // localStorage.setItem('projects_list', JSON.stringify(sub_flush.data));
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

// 修改操作,表格编辑时弹窗和保存
const editVisible = ref(false);
let idx: number = -1;
const editForm = reactive({
  id: '',
  wid: '',
  pid: pid.value,
  p_nickname: '',
  name: '',
  nickname: '',
  crawl_frequency: '',
  description: '',
  status: '',
  modify_user: '',
  extra: '',
});
const handleEdit = (index: number, row: any) => {
  idx = index;
  editForm.id = row.id;
  editForm.wid = row.wid;
  editForm.p_nickname = row.p_nickname;
  editForm.name = row.name;
  editForm.nickname = row.nickname;
  editForm.crawl_frequency = row.crawl_frequency;
  editForm.description = row.description;
  // editForm.status = row.status;
  editForm.modify_user = localStorage.getItem('ms_username') as string;
  // editForm.extra = row.extra;
  editVisible.value = true;
};
const editSaveEdit = async () => {
  if (editForm.nickname) {
    // ElMessage.success(`修改第 ${idx + 1} 行成功`);
    tableData.value[idx].nickname = editForm.nickname;
    tableData.value[idx].description = editForm.description;
    // 向后端发起操作
    const response = (await updateWorkers(editForm));
    if (response.isSuccess) {
      handleFlush();
      ElMessage.success(`修改 ${editForm.nickname} 成功！`);
    } else {
      ElMessage.error(`修改 ${editForm.nickname} 失败！`);
    }
  } else {
    ElMessage.error(`修改 ${editForm.nickname} 失败！项目名称不能为空！`);
  }
  editVisible.value = false;
};

// 密钥信息展示
const upTokenVisible = ref(false);
const upTokenForm = reactive({
  nickname: '',
  name: '',
  wid: '',
});
const handleUpToken = (index: number, row: any) => {
  upTokenForm.nickname = row.nickname;
  upTokenForm.name = row.name;
  upTokenForm.wid = row.wid;
  upTokenVisible.value = true;
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

