<template>
  <div>
    <div class="container">
      <div class="handle-box">
        <el-select v-model="query.filterWord" placeholder="项目名称" class="handle-select mr10">
          <el-option key="1" label="高德地图" value="高德地图"></el-option>
          <el-option key="2" label="美团" value="美团"></el-option>
          <el-option key="2" label="企查查" value="企查查"></el-option>
          <el-option key="2" label="无" value=""></el-option>
        </el-select>
        <el-input v-model="query.keyword" placeholder="搜索词" class="handle-input mr10"></el-input>
        <el-button type="primary" :icon="Search" @click="handleSearch">搜索列表</el-button>
        <el-button type="primary" :icon="Plus" @click="handleFlush">刷新列表</el-button>
      </div>
      <el-table :data="tableData" border class="table" ref="multipleTable" header-cell-class-name="table-header">
        <el-table-column prop="id" label="ID" width="100" align="center"></el-table-column>
        <el-table-column prop="log_project" label="所属项目" width="100"></el-table-column>
        <el-table-column prop="name" label="日志名称"></el-table-column>
        <el-table-column label="日志备注">
          <template #default="scope">{{ scope.row.remarks }}</template>
        </el-table-column>
        <el-table-column prop="address" label="来源ip" width="150"></el-table-column>
        <el-table-column label="操作" width="300" align="center">
          <template #default="scope">
            <el-button text :icon="Edit" @click="handleMonit(scope.$index, scope.row)" v-permiss="15">
              查看
            </el-button>
            <el-button text :icon="Edit" @click="handleEdit(scope.$index, scope.row)" v-permiss="15">
              编辑
            </el-button>
            <el-button text :icon="Delete" class="red" @click="handleDelete(scope.$index)" v-permiss="16">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <div class="pagination">
        <el-pagination
            background
            layout="total, prev, pager, next, jumper"
            :current-page="query.pageIndex"
            :page-size="query.pageSize"
            :total="pageTotal"
            @current-change="handlePageChange"
        ></el-pagination>
      </div>
    </div>

    <!-- 编辑弹出框 -->
    <el-dialog title="编辑" v-model="editVisible" width="30%">
      <el-form label-width="70px">
        <el-form-item label="日志名称">
          <el-input v-model="form.name"></el-input>
        </el-form-item>
        <el-form-item label="来源ip">
          <el-input v-model="form.address"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
				<span class="dialog-footer">
					<el-button @click="editVisible = false">取 消</el-button>
					<el-button type="primary" @click="saveEdit">确 定</el-button>
				</span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts" name="worker_logs">
import {onBeforeMount, reactive, ref} from 'vue';
import {ElMessage, ElMessageBox} from 'element-plus';
import {Delete, Edit, Search, Plus} from '@element-plus/icons-vue';
import {TableItem, query, pageTotal, tableData} from "~/constants/worker_logs";
import {wl_api} from "~/store/worker_logs";
import {getLogs, delLogs} from "~/api/workerLogs";
import {json} from "stream/consumers";

// 刷新数据
const handleFlush = async (init = true) => {
  // 获取数据
  const res = (await getLogs())
  // 是否初始化
  if (init){
    // 载入数据
    tableData.value = res.data.list.slice(0, query.pageSize);
    pageTotal.value = res.data.pageTotal || 1;
    // 缓存数据
    localStorage.setItem('workerLogs', JSON.stringify(res.data));
    // 将查询条件初始化
    query.keyword = ""
    query.filterWord = ""
  }
};
// 打开页面就刷新
handleFlush();

// 分页导航
const handlePageChange = (val: number) => {
  // todo 封装一个函数，对从浏览器缓存中获取数据时，产生的错误进行处理
  let temp = JSON.parse(localStorage.getItem('workerLogs') as string).list;

  // 先筛选后搜索
  if (query.filterWord) {
    temp = wl_api.logProjectFilter(query.filterWord, temp);
    console.log("检测为翻页query.filterWord", query.filterWord)
  } else if (query.keyword) {
    temp = wl_api.keywordSearch(query.keyword, temp);
    console.log("检测为翻页query.keyword", query.keyword)
  } else {
    temp = JSON.parse(localStorage.getItem('workerLogs') as string).list;
  }

  // 对新的搜索结果做分页处理
  query.pageIndex = val;
  pageTotal.value = temp.length || 1;
  console.log("翻页搜索结果datas", temp)
  // 缓存数据
  tableData.value = wl_api.updateView(val, temp);
};

// 查询操作
const handleSearch = () => {
  // 搜索关键词，刷新表格为搜索结果
  let temp = JSON.parse(localStorage.getItem('workerLogs') as string).list
  // let temp:TableItem[] = []

  // 先筛选后搜索
  if (query.filterWord) {
    temp = wl_api.logProjectFilter(query.filterWord, temp);
    console.log("检测为翻页query.filterWord", query.filterWord, temp)
  }

  if (query.keyword) {
    temp = wl_api.keywordSearch(query.keyword, temp);
    console.log("检测为翻页query.keyword", query.keyword, temp)
  }

  if (!temp) {
    temp = JSON.parse(localStorage.getItem('workerLogs') as string).list;
  }

  // 对新的搜索结果做分页处理
  query.pageIndex = 1;
  pageTotal.value = temp.length || 1;
  tableData.value = temp.slice(0, query.pageSize);
};


// 删除操作
const handleDelete = (index: number) => {
  // 二次确认删除
  ElMessageBox.confirm('确定要删除吗？', '提示', {
    type: 'warning'
  })
      .then(async () => { /* 处理正常时 */
        // 获取当前表行数据
        let watiDelData:TableItem = tableData.value.splice(index, 1)[0];
        // 向后端发起删除操作
        const response = (await delLogs(watiDelData));
        if (response.isSuccess) {
          // 响应删除成功则弹出提示
          ElMessage.success('删除成功！');
          // 刷新缓存数据
          const sub_flush = (await getLogs())
          localStorage.setItem('workerLogs', JSON.stringify(sub_flush.data));
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

// 表格编辑时弹窗和保存
const editVisible = ref(false);
let form = reactive({
  name: '',
  address: ''
});

const handleMonit = () => {
  console.log("handleMonit~")
};

let idx: number = -1;
const handleEdit = (index: number, row: any) => {
  idx = index;
  form.name = row.name;
  form.address = row.address;
  editVisible.value = true;
};

const saveEdit = () => {
  editVisible.value = false;
  ElMessage.success(`修改第 ${idx + 1} 行成功`);
  tableData.value[idx].name = form.name;
  tableData.value[idx].address = form.address;
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
