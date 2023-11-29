<template>
	<div>
		<div class="container">
      <div class="plugins-tips">
        <b>项目管理</b>
      </div>
			<div class="handle-box">
				<el-button type="primary" :icon="Plus" @click="handleAdd()">创建项目</el-button>
				<el-button type="primary" :icon="Refresh" @click="handleFlush()">刷新</el-button>
			</div>
      <el-scrollbar>
        <el-table :data="tableData" border class="table" ref="multipleTable" header-cell-class-name="table-header" max-height="550">
          <el-table-column prop="id" label="编号" width="55" align="center"></el-table-column>
          <el-table-column width="350" label="项目名称"  :show-overflow-tooltip="true">
            <template #default="scope">
              <router-link :to="
              { path: '/projects_tabs', query: {
                pid: scope.row.pid,
                name:scope.row.name,
                title:scope.row.name
              }}">{{ scope.row.nickname }}
              </router-link>
<!--              (# 原名: {{ scope.row.name }})-->
            </template>
          </el-table-column>
          <el-table-column label="工作流数量" width="100" :show-overflow-tooltip="true">
            <template #default="scope">
              {{ scope.row.workers_count }}
            </template>
          </el-table-column>
          <el-table-column width="100" label="任务数量" :show-overflow-tooltip="true">
            <template #default="scope">
              {{ scope.row.runing_count }}
            </template>
          </el-table-column>
          <el-table-column width="150" label="所属用户" :show-overflow-tooltip="true">
            <template #default="scope">{{ scope.row.author }}</template>
          </el-table-column>
          <el-table-column width="150" label="委托方/人" :show-overflow-tooltip="true">
            <template #default="scope">{{ scope.row.customer }}</template>
          </el-table-column>
          <el-table-column prop="description" width="300" label="背景描述" :show-overflow-tooltip="true">
          </el-table-column>
          <el-table-column width="200" label="创建时间">
            <template #default="scope">{{ scope.row.create_time }}</template>
          </el-table-column>
          <el-table-column label="操作" width="200" align="center" fixed="right">
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
      </el-scrollbar>

			<div class="pagination">
				<el-pagination
					background
					layout="total, prev, pager, next"
					:current-page="query.pageIndex"
					:page-size="query.pageSize"
					:total="pageTotal"
					@current-change="handlePageChange"
				/>
			</div>
		</div>

		<!-- 弹出框 -->
		<el-dialog title="创建项目" v-model="addVisible" width="40%">
			<el-form label-width="80px">
				<el-form-item label="项目名称">
					<el-input v-model="addForm.name"></el-input>
				</el-form-item>
        <el-form-item label="委托方/人">
          <el-input v-model="addForm.customer"></el-input>
        </el-form-item>
        <el-form-item label="背景描述">
          <el-input type="textarea" v-model="addForm.description"></el-input>
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="addForm.nickname"></el-input>
        </el-form-item>
			</el-form>
			<template #footer>
				<span class="dialog-footer">
					<el-button @click="addVisible = false">取 消</el-button>
					<el-button type="primary" @click="addSaveEdit">确 定</el-button>
				</span>
			</template>
		</el-dialog>

		<el-dialog title="编辑项目" v-model="editVisible" width="40%">
      <el-form label-width="80px">
        <el-form-item label="项目名称">
          <el-input v-model="editForm.nickname"></el-input>
        </el-form-item>
        <el-form-item label="委托方/人">
          <el-input v-model="editForm.customer"></el-input>
        </el-form-item>
        <el-form-item label="背景描述">
          <el-input
              type="textarea"
              v-model="editForm.description"
              placeholder="描述加载中..."
          ></el-input>
        </el-form-item>
<!--        <el-form-item label="权限">-->
<!--          <el-select v-model="editForm.role" placeholder="设置用户权限: admin, test" class="handle-select mr10">-->
<!--            <el-option key="0" label="管理员" value="admin"></el-option>-->
<!--            <el-option key="1" label="普通账户" value="normal"></el-option>-->
<!--          </el-select>-->
<!--        </el-form-item>-->
      </el-form>

			<template #footer>
				<span class="dialog-footer">
					<el-button @click="editVisible = false">取 消</el-button>
					<el-button type="primary" @click="editSaveEdit">确 定</el-button>
				</span>
			</template>
		</el-dialog>
	</div>
</template>

<script setup lang="ts" name="projects_list">
import {ref, reactive, onBeforeMount} from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import {getProjects, addProjects, delProjects, updateProjects} from '~/api/projects';
import { Delete, Edit, Plus,Refresh } from '@element-plus/icons-vue';
interface TableItem {
	id: number;
  pid: string;
	name: string;
	nickname: string;
  description: string;
  author: string;
  customer: string;
  workers_count: number;
  runing_count: number;
  create_time: string;
  update_time: string;
}

const query = reactive({
  filterKey: '',
  filterValue: '',
  keyword: '',
  pageIndex: 1,
  pageSize: 10
});
const tableData = ref<TableItem[]>([]);
const pageTotal = ref(0);

// // 时间格式化
// function formatTimeString(timeString) {
//   console.log(timeString)
//   const date = moment(timeString, 'YYYY-MM-DD HH:mm:ss', true);
//   let temp = date.format('YYYY-MM-DD HH:mm:ss');
//   console.log(temp)
//   return temp;
// }

// 刷新数据
const handleFlush = async (init = true) => {
  // 获取数据
  const res = (await getProjects())
  // 是否初始化
  if (init) {
    // 载入数据
    tableData.value = res.data.list.slice(0, query.pageSize);
    pageTotal.value = res.data.pageTotal || 1;
    // 缓存数据
    localStorage.setItem('projects_list', JSON.stringify(res.data));
  }
};
// 打开页面就刷新
handleFlush();

// 分页导航
const handlePageChange = (val: number) => {
  // todo 封装一个函数，对从浏览器缓存中获取数据时，产生的错误进行处理
  let temp = JSON.parse(localStorage.getItem('projects_list') as string).list;

  // 对新的搜索结果做分页处理
  query.pageIndex = val;
  pageTotal.value = temp.length || 1;
  // console.log("翻页搜索结果datas", temp)
  // 缓存数据
  tableData.value = updateView(val, temp);
};
const updateView = (page_num: number, datas: [] = []) => {
  if (!datas) {
    datas = JSON.parse(localStorage.getItem('workerLogs') as string).list;
  }
  // const datas = JSON.parse(localStorage.getItem('workerLogs') as string).list;
  // 传递页码
  query.pageIndex = page_num;
  // 获取每个分页得大小
  let page_size = query.pageSize
  // 计算本页需要展示得片段
  let index_start = 0
  let index_end = query.pageSize
  if (page_num == 1 /* 第1页和第0页，内容一致 */) {
    index_start = 0
  } else {
    index_start = (page_num - 1) * page_size
    index_end = (page_num - 1) * page_size + page_size
  }
  return datas.slice(index_start, index_end)
};

// 增删改
// 新增操作，表格新增项目时弹窗和保存
const addVisible = ref(false);
let addForm = reactive({
  name: '',
  author: '',
  customer: '',
  description: '',
});
const handleAdd = () => {
  addVisible.value = true;
};
const addSaveEdit = async () => {
  addForm.author = localStorage.getItem('ms_username') as string;
  // 向后端发起操作
  const response = (await addProjects(addForm));
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
  pid: '',
});
const handleDelete = (index: number, row: any) => {
  // 二次确认删除
  ElMessageBox.confirm('确定要删除吗？', '提示', {
    type: 'warning'
  })
      .then(async () => { /* 处理正常时 */
        // 获取当前表行数据
        delform.name = row.name;
        delform.pid = row.pid;
        // 向后端发起删除操作
        const response = (await delProjects(delform));
        if (response.isSuccess) {
          // 响应删除成功则弹出提示
          ElMessage.success('删除成功！');
          // 刷新缓存数据
          const sub_flush = (await getProjects())
          localStorage.setItem('projects_list', JSON.stringify(sub_flush.data));
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
let editForm = reactive({
  pid: '',
  name: '',
  customer: '',
  nickname: '',
  description: '',
});
const handleEdit = (index: number, row: any) => {
	idx = index;
  editForm.pid = row.pid;
  editForm.name = row.name;
  editForm.nickname = row.nickname;
  editForm.customer = row.customer;
  editForm.description = row.description;
  // editForm.nickname = editForm.nickname ? editForm.nickname : row.nickname;
  // editForm.description = editForm.description ? editForm.description : row.description;
  editVisible.value = true;
};
const editSaveEdit = async () => {
  if (editForm.nickname) {
    // ElMessage.success(`修改第 ${idx + 1} 行成功`);
    tableData.value[idx].nickname = editForm.nickname;
    tableData.value[idx].description = editForm.description;
    // 向后端发起操作
    const response = (await updateProjects(editForm));
    if (response.isSuccess) {
      handleFlush();
      ElMessage.success(`修改 ${editForm.name} 成功！`);
    } else {
      ElMessage.error(`修改 ${editForm.name} 失败！`);
    }
  } else {
    ElMessage.error(`修改 ${editForm.name} 失败！项目名称不能为空！`);
  }
  editVisible.value = false;
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
