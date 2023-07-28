<template>
  <div>
    <div class="container">
      <div class="plugins-tips">日志管理</div>
      <div class="handle-box">
        <el-select v-model="query.filterWord" placeholder="所属项目" class="handle-select mr10">
          <el-option  v-for="(item, index) in query.log_projects" :key="index+1" :label="item" :value="item"></el-option>
          <el-option key="0" label="无" value=""></el-option>
        </el-select>
        <el-input v-model="query.keyword" placeholder="搜索词" class="handle-input mr10"></el-input>
        <el-button type="primary" :icon="Search" @click="handleSearch">搜索列表</el-button>
        <el-button type="primary" :icon="Plus" @click="handleFlush">刷新列表</el-button>
      </div>
      <el-table
          :data="tableData"
          border class="table"
          ref="multipleTable"
          header-cell-class-name="table-header"
          min-width="120"
          :show-overflow-tooltip="true">
      >
        <el-table-column prop="id" label="ID" width="300" align="center"></el-table-column>
        <el-table-column prop="name" label="日志名称"></el-table-column>
        <el-table-column prop="log_project" label="所属项目" width="200" :show-overflow-tooltip="true"></el-table-column>
        <el-table-column label="日志备注">
          <template #default="scope">{{ scope.row.remarks }}</template>
        </el-table-column>
        <el-table-column prop="address" label="来源ip" width="200"></el-table-column>
        <el-table-column label="操作" width="300" align="center">
          <template #default="scope">
            <el-button text :icon="Edit" @click="handleMonit(scope.$index, scope.row)" v-permiss="15">
              查看
            </el-button>
            <el-button text :icon="Edit" @click="handleEdit(scope.$index, scope.row)" v-permiss="100">
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

    <!-- 日志查看弹出框 -->
    <el-dialog
        v-model="logVisible"
        title="查看日志"
        width="50%"
        :fullscreen="fullscreen"
        :before-close="handleClose"
        :show-close="false"
        :close-on-click-modal="false"
        destroy-on-close
    >
      <!-- 弹窗头部 -->
      <template #header="{ close, titleId, titleClass, scope }">
        <div class="my-header">
          <h4 :id="titleId" :class="titleClass">查看日志</h4>
          <div class="dialog-header-right">
            <el-button link :icon="RefreshRight" @click="handleLogContent"></el-button>
            <el-button link :icon="FullScreen" @click="changeScreen"></el-button>
            <el-button link :icon="Close" @click="close"></el-button>
          </div>
        </div>
      </template>

      <el-input
          v-model="logTextarea"
          :autosize="{ minRows: 10, maxRows: 20 }"
          :readonly="false"
          type="textarea"
          placeholder="日志加载中..."
          class="log-text"
      />

      <template #footer>
      <span class="dialog-footer">
        <el-button type="primary" @click="fullscreen = false; logVisible = false;">
          关闭
        </el-button>
      </span>
      </template>
    </el-dialog>

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
import {Delete, Edit, Search, Plus, FullScreen, Close, RefreshRight} from '@element-plus/icons-vue';
import {TableItem, textAreaItem, query, pageTotal, tableData, editVisible, form} from "~/constants/worker_logs";
import {wl_api} from "~/store/worker_logs";
import {getLogs, delLogs, getLogContent} from "~/api/workerLogs";

// 刷新数据
const handleFlush = async (init = true) => {
  // 获取数据
  const res = (await getLogs())
  // 是否初始化
  if (init) {
    // 载入数据
    tableData.value = res.data.list.slice(0, query.pageSize);
    pageTotal.value = res.data.pageTotal || 1;
    // 缓存数据
    localStorage.setItem('workerLogs', JSON.stringify(res.data));
    // 将查询条件初始化
    query.keyword = ""
    query.filterWord = ""
    query.log_projects = res.data.log_projects
    console.log("res.data.log_projects",res.data.log_projects)
    console.log("query.log_projects",query.log_projects)
  }
};
// 打开页面就刷新
handleFlush();

// 分页操作
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
        // let watiDelData: TableItem = tableData.value.splice(index, 1)[0];
        let watiDelData: TableItem = tableData.value[index];
        console.log("watiDelData", watiDelData)
        // 向后端发起删除操作
        const response = (await delLogs(watiDelData));
        if (response.isSuccess) {
          // 响应删除成功则弹出提示
          ElMessage.success('删除成功！');
          // 刷新缓存数据
          const sub_flush = (await getLogs())
          localStorage.setItem('workerLogs', JSON.stringify(sub_flush.data));
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

// 定位待处理行的下标
let idx: number = -1;
// 日志内容查看
// 日志窗口的显示开关
const logVisible = ref(false)
// 日志窗口待操作的变量
let logMointForm = reactive({
  id: '',
  log_project: '',
  name: '',
  remarks: '',
  address: '',
  create_time: 0,
  modify_time: 0,
})

// 日志窗口处理器（void类型表示函数没有返回值）
const handleMonit = (index: number, row: any, done: () => void) => {
  idx = index;
  logMointForm.id = row.id;
  logMointForm.log_project = row.log_project;
  logMointForm.name = row.name;
  logMointForm.remarks = row.remarks;
  logMointForm.address = row.address;
  logVisible.value = true;
  // 获取日志文本
  handleLogContent(index,row)
  console.log("handleMonit~")
};
//全屏
const fullscreen = ref(false)

let minRows = ref(10)
let maxRows = ref(20)
// let textArea = {
//   "minRows":minRows,
//   "maxRows":maxRows,
// }
const changeScreen = () => {
  if (fullscreen.value == true) {
    fullscreen.value = false;
    minRows.value = 10
    maxRows.value = 20
    console.log("textAreaRows true", minRows, maxRows)
  } else {
    fullscreen.value = true;
    minRows.value = 50
    maxRows.value = 100
    console.log("textAreaRows false", minRows, maxRows)
  }
  //fullscreen.value = !fullscreen.value;
}

// 弹窗关闭确认
const handleClose = (done: () => void) => {
  // 弹窗关闭确认，:before用法的实践
  ElMessageBox.confirm('确定要退出日志查看吗?')
      .then(() => {
        done()
        changeScreen()
      })
      .catch(() => {
        // catch error
      })
}

// 获取日志文件内容
// 日志文本容器
const logTextarea = ref('')
const handleLogContent = async (index: number, row: any) => {
  let watiGetInfo: TableItem = row ?? logMointForm;
  // console.log("row", row)
  // console.log("watiGetInfo", watiGetInfo)
  const response = (await getLogContent(watiGetInfo))
  logTextarea.value = response.data.content
}


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

/*.el-input__inner .log-text {*/
/*  background-color: #67C23A;*/
/*  color: #000;*/
/*}*/


/* raw */

.dialog-footer button:first-child {
  margin-right: 10px;
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
