<template>
  <div>
    <div class="container">
      <div class="plugins-tips">
        <b>任务告警</b>
      </div>
      <div class="handle-box">
        <el-button type="primary" :icon="Plus" @click="handleAdd();handleCascader();">创建监控</el-button>
        <el-button type="primary" :icon="Refresh" @click="handleFlush();">刷新</el-button>
      </div>
      <el-scrollbar>
        <el-table :data="tableData" border class="table" ref="multipleTable" header-cell-class-name="table-header">
          <el-table-column prop="id" label="编号" width="55" align="center"></el-table-column>
          <el-table-column prop="name" label="名称" :show-overflow-tooltip="true"></el-table-column>
          <el-table-column prop="delivery" label="开/关" width="80">
            <template #default="scope">
              <el-switch
                  v-model="scope.row.delivery"
                  :active-value='1'
                  :inactive-value='0'
                  @change="handleSwitchChange(scope.row)"
              >
              </el-switch>
            </template>
          </el-table-column>
          <el-table-column prop="resource" label="类型" width="100" :show-overflow-tooltip="true"></el-table-column>
          <el-table-column prop="desc" width="200" label="描述" :show-overflow-tooltip="true"></el-table-column>
          <el-table-column width="200" label="创建时间">
            <template #default="scope">{{ scope.row.create_time }}</template>
          </el-table-column>
          <el-table-column label="操作" width="200" align="center" fixed="right">
            <template #default="scope">
              <el-button text :icon="Edit" @click="handleEdit(scope.$index, scope.row)" v-permiss="15">
                信息
              </el-button>
              <el-button text :icon="Delete" class="red" @click="handleDelete(scope.$index, scope.row)" v-permiss="16">
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-scrollbar>
      <div class="pagination">
        <el-pagination
            background
            layout="total, prev, pager, next"
            :current-page="alarm_query.pageIndex"
            :page-size="alarm_query.pageSize"
            :total="pageTotal"
            @current-change="handlePageChange"
        ></el-pagination>
      </div>
    </div>

    <!-- 弹出框 -->
    <el-dialog title="创建监控" v-model="addVisible" width="30%">
      <el-form label-width="100px">
        <el-form-item label="监控名称">
          <el-input v-model="addForm.name"></el-input>
        </el-form-item>

        <el-form-item label="工作流">
          <el-cascader :options="cascader" @change="handleCascaderChange">
            <template #default="{ node, data }">
              <span>{{ data.label }}</span>
              <span v-if="!node.isLeaf"> ({{ data.children.length }}) </span>
            </template>
          </el-cascader>
        </el-form-item>
        <el-form-item label="密钥">
          <el-input v-model="addForm.wid" :disabled="true"></el-input>
        </el-form-item>

        <el-form-item label="告警器">
          <el-select v-model="addForm.aid" placeholder="告警器">
            <el-option v-for="(item, index) in alarmers_list" :key="item.aid"
                       :label="item.resource + '_' + item.name" :value="item.aid"
                       @click="handleAddResource(item.resource)"
            >
            </el-option>
            <el-option key="0" label="无" value=""></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="告警类型">
          <el-input v-model="addForm.resource" disabled></el-input>
        </el-form-item>
        <el-form-item label="监控描述">
          <el-input type="textarea" v-model="addForm.desc"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
				<span class="dialog-footer">
					<el-button @click="addVisible = false">取 消</el-button>
					<el-button type="primary" @click="addSaveEdit">确 定</el-button>
				</span>
      </template>
    </el-dialog>

    <el-dialog title="任务信息" v-model="editVisible" width="40%">
      <el-form label-width="100px">
        <el-form-item v-for="(value, key) in editForm" :key="key" :label="key">
          <el-input
              v-if="typeof value === 'string'"
              v-model="editForm[key]"
          ></el-input>
        </el-form-item>
      </el-form>

<!--      <el-form label-width="100px">-->
<!--        <el-form-item v-for="(value, key) in worker_info" :key="key" :label="key">-->
<!--          <el-input-->
<!--              v-if="typeof value === 'string'"-->
<!--              v-model="worker_info[key]"-->
<!--          ></el-input>-->
<!--        </el-form-item>-->
<!--      </el-form>-->

      <template #footer>
				<span class="dialog-footer">
					<el-button @click="editVisible = false">关闭</el-button>
				</span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts" name="projects_list">
import {reactive, ref, onMounted} from 'vue';
import {ElMessage, ElMessageBox} from 'element-plus';
import {addAlarmerJobs, delAlarmerJobs, getAlarmerJobs, getAlarmers, updateAlarmerJobs, getProSub} from '~/api/alarms';
import { Delete, Edit, Plus,Refresh } from '@element-plus/icons-vue';
import {getWorker} from '~/api/projects';
// import {um_api} from "~/store/user_mange";
import type { CascaderProps } from 'element-plus'

interface TableItem {
  id: number;
  a_jid: string,
  wid: string,
  aid: string,
  name: string,
  delivery: number,
  resource: string,
  desc: string,
  alarm_content: string,
  extra: string;
  create_time: string;
}

interface alarmers_TableItem {
  id: number;
  aid: string,
  name: string,
  email: string,
  qw_token: string,
  resource: string,
  desc: string,
  extra: string;
  create_time: string;
}

const alarm_query = reactive({
  filterWord: '',
  keyword: '',
  pageIndex: 1,
  pageSize: 100
})
// const query = alarm_query
const tableData = ref<TableItem[]>([]);
const pageTotal = ref(0);


// 刷新数据
const handleFlush = async (init = true) => {
  // 获取数据
  const res = (await getAlarmerJobs())
  // 是否初始化
  if (init) {
    // 载入数据
    tableData.value = res.data.list.slice(0, alarm_query.pageSize);
    pageTotal.value = res.data.pageTotal || 1;
    // 缓存数据
    localStorage.setItem('alarmerJobs_list', JSON.stringify(res.data));
  }
};
// 打开页面就刷新
// handleFlush();

// 列表刷新展示
const updateView = (page_num: number, datas: [] = []) => {
  if (!datas) {
    datas = JSON.parse(localStorage.getItem('alarmerJobs_list') as string).list;
  }
  // 传递页码
  alarm_query.pageIndex = page_num;
  // 获取每个分页得大小
  let page_size = alarm_query.pageSize
  // 计算本页需要展示得片段
  let index_start = 0
  let index_end = alarm_query.pageSize
  if (page_num == 1 /* 第1页和第0页，内容一致 */) {
    index_start = 0
  } else {
    index_start = (page_num - 1) * page_size
    index_end = (page_num - 1) * page_size + page_size
  }
  return datas.slice(index_start, index_end)
}

// 分页导航
const handlePageChange = (val: number) => {
  // todo 封装一个函数，对从浏览器缓存中获取数据时，产生的错误进行处理
  let temp = JSON.parse(localStorage.getItem('alarmerJobs_list') as string).list;

  // 对新的搜索结果做分页处理
  alarm_query.pageIndex = val;
  pageTotal.value = temp.length || 1;
  console.log("翻页搜索结果datas", temp)
  // 缓存数据
  tableData.value = updateView(val, temp);
};

// 增删改
// 新增操作，表格新增项目时弹窗和保存
const addVisible = ref(false);
let addForm = reactive({
  name: '',
  aid: '',
  wid: '',
  resource: '',
  desc: '',
});
const alarmers_list = ref<alarmers_TableItem[]>([]);
const handleAddResource = (resource: string) => {
  // 将resource数据填入到 addForm
  addForm.resource = resource
}
const handleAdd = async () => {
  // 获取告警器列表,用于下来选择
  const response = (await getAlarmers())
  alarmers_list.value = response.data.list
  addVisible.value = true;
};
const addSaveEdit = async () => {
  // 向后端发起操作
  const response = (await addAlarmerJobs(addForm));
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
  name: '',
  a_jid: '',
});
const handleDelete = (index: number, row: any) => {
  // 二次确认删除
  ElMessageBox.confirm('确定要删除吗？', '提示', {
    type: 'warning'
  })
      .then(async () => { /* 处理正常时 */
        // 获取当前表行数据
        delform.name = row.name;
        delform.a_jid = row.a_jid;
        // 向后端发起删除操作
        const response = (await delAlarmerJobs(delform));
        if (response.isSuccess) {
          // 响应删除成功则弹出提示
          ElMessage.success('删除成功！');
          // 刷新缓存数据
          const sub_flush = (await getAlarmerJobs())
          localStorage.setItem('alarmerJobs_list', JSON.stringify(sub_flush.data));
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

// 开关切换
let switchform = reactive({
  id: 0,
  name: '',
  a_jid: '',
  aid: '',
  delivery: 0,
});
const handleSwitchChange = async (row: any) => {
  switchform.id = row.id
  switchform.name = row.name
  switchform.aid = row.aid
  switchform.a_jid = row.a_jid
  switchform.delivery = parseInt(row.delivery);
  // 获取数据
  const response = (await updateAlarmerJobs(switchform))
  if (response.isSuccess) {
    ElMessage.success('开关切换成功！');
  } else {
    ElMessage.error('开关切换失败！');
  }

  // 在这里可以处理开关状态变化后的逻辑
  console.log("开关",row.delivery)
};

// 修改操作,表格编辑时弹窗和保存
const editVisible = ref(false);
let idx: number = -1;
let editForm = reactive({
  监控编号: '',
  监控目标: '',
  监控名称: '',
  监控描述: '',
});
let worker_info = reactive({
  受控目标名称: '',
  受控所属项目: '',
  受控目标描述: '',
})
const handleEdit = async (index: number, row: any) => {
  // 获取被监控工作流的信息
  const response = (await getWorker({wid: row.wid}))
  const worker_info = response.data
  console.log(worker_info)
  idx = index;
  editForm.监控目标 = row.wid;
  editForm.监控编号 = row.a_jid;
  editForm.监控名称 = row.name;
  editForm.监控描述 = row.desc;
  worker_info.受控目标名称 = worker_info.name;
  worker_info.受控所属项目 = worker_info.p_nickname;
  worker_info.受控目标描述 = worker_info.description;
  editVisible.value = true;
};

// 获取项目和工作流的自从关系
// 作为级联选择器
let cascader = []
const handleCascader = async () => {
  const response = (await getProSub())
  cascader = response.data.list
  console.log("cascader:",cascader)
}
const handleCascaderChange = (value:string) => {
  // 获取最后一级选项的value
  const lastValue:string = value[value.length - 1];

  // 将其赋值给addForm.wid
  addForm.wid = lastValue || '';
}

onMounted(() => {
  handleFlush();
  handleCascader();
});

</script>

<style scoped>
.custom-cascader {
  width: 30%;
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
