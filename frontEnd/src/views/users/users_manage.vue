<template>
	<div>
		<div class="container">
      <div class="plugins-tips">账号管理</div>
			<div class="handle-box">
				<el-input v-model="query.keyword" placeholder="用户名" class="handle-input mr10"></el-input>
				<el-button type="primary" :icon="Search" @click="handleSearch">搜索</el-button>
				<el-button type="primary" :icon="Plus" @click="handleAdd">新增</el-button>
				<el-button type="primary" :icon="Refresh" @click="handleFlush">刷新</el-button>
			</div>
			<el-table :data="tableData" border class="table" ref="multipleTable" header-cell-class-name="table-header">
				<el-table-column prop="id" label="ID" width="55" align="center"></el-table-column>
				<el-table-column prop="name" label="用户名"></el-table-column>
				<el-table-column label="昵称">
					<template #default="scope">{{ scope.row.nicename }} #{{ scope.row.id }}</template>
				</el-table-column>
				<el-table-column prop="role" label="权限等级">
          <template #default="scope">{{
              scope.row.role === "admin" ? '管理者' :
              scope.row.role === "xadmin" ? '开发者' :
              scope.row.role === 'coder' ? '开发者' :
              scope.row.role === 'normal' ? '使用者' :
              '未知'
            }}</template>
        </el-table-column>
				<el-table-column label="状态" align="center">
					<template #default="scope">
						<el-tag
							:type="scope.row.status === '1' ? 'success' : scope.row.status === '0' ? 'danger' : ''"
						>
							{{ scope.row.status === '1' ? '启用' : scope.row.status === '0' ? '禁用' : ''}}
						</el-tag>
					</template>
				</el-table-column>

				<el-table-column prop="create" label="注册时间"></el-table-column>
				<el-table-column label="操作" width="220" align="center">
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
			<div class="pagination">
				<el-pagination
					background
					layout="total, prev, pager, next"
					:current-page="query.pageIndex"
					:page-size="query.pageSize"
					:total="pageTotal"
					@current-change="handlePageChange"
				></el-pagination>
			</div>
		</div>

		<!-- 编辑弹出框 -->
		<el-dialog title="新增用户" v-model="addVisible" width="30%">
			<el-form label-width="70px">
				<el-form-item label="用户名">
					<el-input v-model="addForm.name"></el-input>
				</el-form-item>
				<el-form-item label="昵称">
					<el-input v-model="addForm.nicename"></el-input>
				</el-form-item>
        <el-form-item label="密码">
          <el-input v-model="addForm.password"></el-input>
        </el-form-item>
        <el-form-item label="权限">
          <el-input v-model="addForm.role"></el-input>
        </el-form-item>
			</el-form>
			<template #footer>
				<span class="dialog-footer">
					<el-button @click="addVisible = false">取 消</el-button>
					<el-button type="primary" @click="addSaveEdit">确 定</el-button>
				</span>
			</template>
		</el-dialog>

		<el-dialog title="编辑" v-model="editVisible" width="30%">

      <el-form label-width="70px">
        <el-form-item label="昵称">
          <el-input v-model="editForm.nicename"></el-input>
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="editForm.password"></el-input>
        </el-form-item>
        <el-form-item label="权限">
          <el-select v-model="editForm.role" placeholder="设置用户权限: admin, test" class="handle-select mr10">
            <el-option key="0" label="管理员" value="admin"></el-option>
            <el-option key="1" label="使用者" value="normal"></el-option>
            <el-option key="1" label="开发员" value="normal"></el-option>
          </el-select>
        </el-form-item>
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

<script setup lang="ts" name="basetable">
import { ref, reactive } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { Delete, Edit, Search, Plus, Refresh } from '@element-plus/icons-vue';
import {add_user, edit_user, get_users, del_user} from '~/api/account';
import {um_api} from "~/store/user_mange";

interface TableItem {
	id: number;
	name: string;
  nicename: string;
	status: string;
	create: string;
  role: string;
  password: string;
  lastlogin: string;
}

const query = um_api.query
const tableData = ref<TableItem[]>([]);
const pageTotal = ref(0);
// 获取表格数据
// import { fetchData } from '~/api/index';
// const getData = () => {
// 	fetchData().then(res => {
// 		tableData.value = res.data.list;
// 		pageTotal.value = res.data.pageTotal || 50;
// 	});
// };
// getData();

// 刷新数据
const handleFlush = async (init = true) => {
  // 获取数据
  const res = (await get_users())
  // 是否初始化
  if (init) {
    // 载入数据
    tableData.value = res.data.list.slice(0, query.pageSize);
    pageTotal.value = res.data.pageTotal || 1;
    // 缓存数据
    localStorage.setItem('users_manage', JSON.stringify(res.data));
  }
};
// 打开页面就刷新
handleFlush();

// 分页导航
const handlePageChange = (val: number) => {
  // todo 封装一个函数，对从浏览器缓存中获取数据时，产生的错误进行处理
  let temp = JSON.parse(localStorage.getItem('workerLogs') as string).list;

  // 搜索
 if (query.keyword) {
    temp = um_api.keywordSearch(query.keyword, temp);
    console.log("检测为翻页query.keyword", query.keyword)
  } else {
    temp = JSON.parse(localStorage.getItem('workerLogs') as string).list;
  }

  // 对新的搜索结果做分页处理
  query.pageIndex = val;
  pageTotal.value = temp.length || 1;
  console.log("翻页搜索结果datas", temp)
  // 缓存数据
  tableData.value = um_api.updateView(val, temp);
};

// 查询操作
const handleSearch = () => {
  // 搜索关键词，刷新表格为搜索结果
  let temp = JSON.parse(localStorage.getItem('users_manage') as string).list
  console.log(temp)
  console.log(query.keyword)
  // let temp:TableItem[] = []

  if (query.keyword) {
    temp = um_api.keywordSearch(query.keyword, temp);
    console.log("检测为翻页query.keyword", query.keyword, temp)
  }

  if (!temp) {
    temp = JSON.parse(localStorage.getItem('users_manage') as string).list;
  }

  // 对新的搜索结果做分页处理
  query.pageIndex = 1;
  pageTotal.value = temp.length || 1;
  tableData.value = temp.slice(0, query.pageSize);
};

// 删除操作
let delform = reactive({
  id: '',
  name: '',
  nicename: '',
  role: '',
});
const handleDelete = (index: number, row: any) => {
  // 二次确认删除
  ElMessageBox.confirm('确定要删除吗？', '提示', {
    type: 'warning'
  })
      .then(async () => { /* 处理正常时 */
        // 获取当前表行数据
        delform.id = row.id;
        delform.name = row.name;
        delform.nicename = row.nicename;
        delform.role = row.role;
        // 向后端发起删除操作
        const response = (await del_user(delform));
        if (response.isSuccess) {
          // 响应删除成功则弹出提示
          ElMessage.success('删除成功！');
          // 刷新缓存数据
          const sub_flush = (await get_users())
          localStorage.setItem('users_manage', JSON.stringify(sub_flush.data));
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

// 表格新增时弹窗和保存
const addVisible = ref(false);
let addForm = reactive({
  name: '',
  nicename: '',
  password: '',
  role: '',
});
const handleAdd = () => {

  addVisible.value = true;
};
const addSaveEdit = async () => {
  // 向后端发起操作
  const response = (await add_user(addForm));
  if (response.isSuccess) {
    addVisible.value = false;
    handleFlush();
    ElMessage.success(`新增 ${addForm.name} 成功！`);
  } else {
    ElMessage.error(`新增 ${addForm.name} 失败！`);
  }
};

// 表格编辑时弹窗和保存
let editVisible = ref(false);
let editForm = reactive({
  id: '',
  name: '',
  nicename: '',
  password: '',
  role: '',
});
let idx: number = -1;
const handleEdit = (index: number, row: any) => {
	idx = index;
  editForm.id = row.id;
  editForm.name = row.name;
  editForm.nicename = row.nicename;
  editForm.password = row.password;
	editVisible.value = true;

};
const editSaveEdit = async () => {
	// ElMessage.success(`修改第 ${idx + 1} 行成功`);
	tableData.value[idx].nicename = editForm.nicename;
	tableData.value[idx].role = editForm.role;
  // 向后端发起操作
  const response = (await edit_user(editForm));
  if (response.isSuccess) {
    handleFlush();
    ElMessage.success(`修改 ${editForm.name} 成功！`);
  } else {
    ElMessage.error(`修改 ${editForm.name} 失败！`);
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
