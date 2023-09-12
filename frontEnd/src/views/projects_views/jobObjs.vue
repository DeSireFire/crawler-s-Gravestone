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
      <el-input v-model="query.keyword" placeholder="搜索列表" class="handle-input mr10">
        <template #append>
          <el-button :icon="Search" @click="filterEdit()"/>
        </template>
      </el-input>
      <el-button type="primary" :icon="Search" @click="filterVisible = true;">高级筛选</el-button>
      <el-button type="primary" :icon="Refresh" @click="handleFlush()">刷新列表</el-button>
    </div>
    <el-scrollbar>
      <el-table
        :data="tableResData"
        :border="true"
        stripe
        class="table"
        @sort-change="handleSortChange"

        header-cell-class-name="table-header"
        height="540"
      >
      <!--:default-sort="{ prop: 'end_time', order: 'null' }"-->
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

        <!-- 错误列添加排序功能 -->
        <el-table-column class-name="log-num" width="100" label="错误"
                         :show-overflow-tooltip="true" prop="log_lv_error"
                         sortable :sort-method="customSortMethod('log_lv_error')">
          <template #default="scope">
            <span class="error-color">{{ scope.row.log_lv_error }}</span>
          </template>
        </el-table-column>

        <!-- 警告列添加排序功能 -->
        <el-table-column class-name="log-num" width="100" label="警告"
                         :show-overflow-tooltip="true" prop="log_lv_warning"
                         sortable :sort-method="customSortMethod('log_lv_warning')">
          <template #default="scope">
            <span class="warning-color">{{ scope.row.log_lv_warning }}</span>
          </template>
        </el-table-column>

        <!-- 常规列添加排序功能 -->
        <el-table-column class-name="log-num" width="100" label="常规"
                         :show-overflow-tooltip="true" prop="log_lv_info"
                         sortable :sort-method="customSortMethod('log_lv_info')">
          <template #default="scope">
            <span class="info-color">{{ scope.row.log_lv_info }}</span>
          </template>
        </el-table-column>

        <!-- 数据计数列添加排序功能 -->
        <el-table-column class-name="log-num" width="200" label="数据计数"
                         :show-overflow-tooltip="true"
                         prop="items_count"
                         sortable :sort-method="customSortMethod('items_count')">
          <template #default="scope">
            <span class="ok-color">{{ scope.row.items_count }}</span>
          </template>
        </el-table-column>

        <el-table-column width="100" label="执行用户" :show-overflow-tooltip="true">
          <template #default="scope">{{ scope.row.run_user }}</template>
        </el-table-column>
        <el-table-column width="140" label="记录开始时间" prop="create_time"
                         sortable :sort-method="sortTime('create_time')">
          <template #default="{ row }">{{ formatDate(row.create_time) }}</template>
        </el-table-column>
        <el-table-column width="140" label="记录结束时间" prop="end_time"
                         sortable :sort-method="sortTime('end_time')">
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

    <!-- 分页组件 -->
    <div class="pagination">
      <el-pagination
          background
          layout="total, sizes, prev, pager, next, jumper"
          v-model="query.pageIndex"
          v-model:page-size="query.pageSize"
          :page-sizes="[10, 20, 30, 40, 50, 100]"
          :pager-count="5"
          :page-size="query.pageSize"
          :total="pageTotal"
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
      />
    </div>

    <!--  功能弹窗  -->
    <el-dialog title="高级搜索" v-model="filterVisible" width="30%">
      <el-form label-width="80px">
        <el-form-item label="筛选词:">
          <el-input v-model="query.filterValue"
                    placeholder="匹配的筛选值"
                    class="input-with-select"
                    style="width: 400px"
                    clearable
          >
            <template #prepend>
              <el-select v-model="query.filterKey" style="width: 150px" placeholder="选择列名">
                <el-option
                    v-for="(option, columnName) in columnOptions"
                    :key="columnName"
                    :label="option.value"
                    :value="option.label"
                    @click="query.filterKey = option.label"
                />
                <el-option key="0" label="无" value=""></el-option>
              </el-select>
            </template>
          </el-input>
        </el-form-item>

        <el-form-item label="搜索词:">
          <el-input v-model="query.keyword" style="width: 400px"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
				<span class="dialog-footer">
          <el-button @click="clearQuery">重 置</el-button>
					<el-button @click="filterVisible = false">取 消</el-button>
					<el-button type="primary" @click="filterEdit();">确 定</el-button>
				</span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts" name="sub_jobObj">
import { ref, reactive, computed, nextTick } from 'vue';
import { useRoute } from 'vue-router';
import { ElMessage, ElMessageBox } from 'element-plus';
import {getJobs, delJobs, getLogContent, getProjectsNames, addProjects} from '~/api/projects';
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
  filterKey: '',
  filterValue: '',
  keyword: '',
  pageIndex: 1,
  pageSize: 10,
});
// 表格原始数据
const tableRawData = ref<TableItem[]>([]);
// 表格整合数据
const tableResData = ref<TableItem[]>([]);

const pageTotal = ref(0);

// 初始化query数据
const clearQuery = () => {
  query.filterKey = ''
  query.filterValue = ''
  query.keyword = ''
  query.pageIndex = 1
  query.pageSize = 10
};

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
    tableRawData.value = res.data.list.slice(0, query.pageSize);
    if (tableRawData.value) {
      tableResData.value = tableRawData.value
    }
    pageTotal.value = res.data.pageTotal || 1;

    // 清空筛选器
    query.filterKey = '';
    query.filterValue = '';
    query.keyword = '';

    // 缓存数据
    localStorage.setItem('jobs_list', JSON.stringify(res.data));
  }
};
// 打开页面就刷新
handleFlush();

// 声明 jobsList 和 keyword 的类型
let jobsList: { list: TableItem[] };
// 表格数据处理
const handleTableDataResult = async () => {
  // 初始化中间变量
  let temp:TableItem[] = [];

  // 数据来源：后台获取、缓存读取
  // 从localStorage中获取缓存数据
  jobsList = JSON.parse(localStorage.getItem('jobs_list') as string);

  // 如果缓存数据不存在，运行handleFlush函数并重新获取
  if (!jobsList) {
    handleFlush();
    jobsList = JSON.parse(localStorage.getItem('jobs_list') as string);
  }
  temp = jobsList.list;

  // 筛选数据：根据特定条件，对数据筛选
  if (query.filterValue && query.filterKey) {
    temp = handleFilter(temp);
  }

  // 搜索数据：根据给出的关键词，对数据包含筛选
  if (query.keyword) {
    temp = handleSearch(temp);
  }

  // 数据排序：根据生成的数据进行排序
  // temp.sort("end_time", "descending")
  // temp.sort((a:TableItem, b:TableItem) => parseInt(a.end_time.toString()) - parseInt(b.end_time.toString()));

  // 统计数据：筛选完后对数据总数进行记录，为之后的分页做准备
  // console.log("temp.length",temp.length)
  pageTotal.value = temp.length || 1;

  // 翻页处理：获取当前页数，计算经过过滤以后列表数据的分页，没超过总页数，直接翻页，超过直接返回第一页。
  // console.log("当前页数", query.pageIndex)
  if (query.pageIndex >= 1) {
    let cursor_start = (parseInt(query.pageIndex) - 1) * parseInt(query.pageSize)
    let cursor_end = cursor_start + parseInt(query.pageSize)
    temp = temp.slice(cursor_start, cursor_end);
  } else {
    temp = temp.slice(0, query.pageSize);
  }

  // 装载数据：将多重处理后的数据交给表格渲染
  tableResData.value = temp;
  // console.log("tableResData",tableResData.value)
}

// 条件过滤
// 定义筛选数据的函数
const columnMapping = {
  // 'id': '编号',
  // 'name': '实例名称',
  'status': '状态',
  'p_nickname': '所属项目',
  // 'w_nickname': '工作流',
  // 'log_lv_error': '错误',
  // 'log_lv_warning': '警告',
  // 'log_lv_info': '常规',
  // 'items_count': '数据计数',
  'run_user': '执行用户',
  // 'create_time': '记录开始时间',
  // 'end_time': '记录结束时间',
};
// 计算属性，提取表格列名并创建选项
const columnOptions = computed(() => {
  const options = [];
  if (tableRawData.value.length > 0) {
    const firstRow = tableRawData.value[0];
    for (const columnName in firstRow) {
      // 检查是否存在于映射中
      if (columnMapping[columnName as keyof typeof columnMapping]) {
        const variableName = columnMapping[columnName as keyof typeof columnMapping];
        options.push({ label: columnName, value: variableName });
      }
    }
  }
  return options;
});
// 响应式数据，用于存储用户选择的列名
const handleFilter = (temp: TableItem[] = []) => {
  // 传入需要筛选的值和被查询的字段名称
  if (!query.filterKey || !query.filterValue) {
    return temp;
  }

  let temp_fk = ""
  let temp_fv:any = ""

  console.log("query.filterKey",query.filterKey)
  console.log("query.filterValue",query.filterValue)
  // 检查 query.filterKey 是否存在于 TableItem 的键名列表中
  const validKeys: (keyof TableItem)[] = Object.keys(temp[0]) as (keyof TableItem)[];
  if (!validKeys.includes(query.filterKey as keyof TableItem)) {
    console.error(`Invalid filterKey: ${query.filterKey}`);
    return temp;
  }

  temp_fk = query.filterKey
  temp_fv = query.filterValue

  // 状态 列 参数的转换 特化代码
  if (query.filterKey && query.filterKey=="status") {
    let qfv = ['未知', '执行中', '结束', '中断', '失败'].findIndex(status => status === query.filterValue)
    temp_fv = qfv as number;
  }
  console.log(temp_fk, temp_fv)
  console.log(temp)
  const filteredData = temp.filter(item => item[temp_fk as keyof TableItem] === temp_fv);
  console.log(`筛选结果：`, filteredData);
  // 清空
  temp_fk = "";
  temp_fv = "";
  return filteredData;
};

// 关键词搜索
let keyword: string = '';
// 处理搜索逻辑
const handleSearch = (temp:TableItem[]=[]) => {
  if (!temp.length) {
    // 从localStorage中获取缓存数据
    jobsList = JSON.parse(localStorage.getItem('jobs_list') as string);

    // 如果缓存数据不存在，运行handleFlush函数并重新获取
    if (!jobsList) {
      handleFlush();
      jobsList = JSON.parse(localStorage.getItem('jobs_list') as string);
    }

    temp = jobsList.list;
  }

  // 从列表数据中根据关键词搜索匹配项
  if (temp && query.keyword) {
    keyword = query.keyword.trim();
    temp = temp.filter(item => item.name.includes(keyword));
  }

  return temp
};

// 数据排序
// 时间排序
const sortKey = ref('create_time');
const sortOrder = ref('descending');
// 时间日期排序
const sortTime = (propName: string) => {
  // console.log("propName:",propName)
  return (a: any, b: any) => {
    const dateA = new Date(a[propName]);
    const dateB = new Date(a[propName]);
    return dateA.getTime() - dateB.getTime();
  }
};
// 各项计数排序
const customSortMethod = (propName: string) => {
  return (a: any, b: any) => {
    // 从 a 和 b 中获取指定字段的值进行比较
    const valA = parseFloat(a[propName]);
    const valB = parseFloat(b[propName]);

    // 否则，按数字大小升序排序
    return valA - valB;
  };
};


// 排序处理
const handleSortChange = ({ column, prop, order }: any) => {
  sortKey.value = prop;
  sortOrder.value = order;
  // console.log("column",column)
  // console.log("prop",prop)
  // console.log("order",order)
};

// 分页操作
const handlePageChange = (pageNumber: number) => {
  query.pageIndex = pageNumber
  handleTableDataResult();
};
// 单页展示数量设置
const handleSizeChange = (pageSize: number) => {
  query.pageSize = pageSize
  handleTableDataResult();
}

// 时间戳转date格式进行展示
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
          // 刷新缓存数据
          const sub_flush = (await getJobs({}))
          console.log("sub_flush", sub_flush)
          localStorage.setItem('jobs_list', JSON.stringify(sub_flush.data));

          // todo 旧版bug待修复
          let temp = tableResData.value.splice(index, 1)[0];
          tableResData.value = sub_flush.data.list
          pageTotal.value -= 1

          // // todo 根据刷新的数据处理筛选条件
          // handleTableDataResult();

          // 响应删除成功则弹出提示
          ElMessage.success('删除成功！');

        } else {
          // 响应删除失败则弹出错误
          throw new Error(response.errMsg);
        }
      })
      .catch((error) => { /* 处理失败时 */
        ElMessage.error(`删除失败! ${error}`);
      });
};

// 高级搜索 弹窗
const filterVisible = ref(false);
const filterEdit = async () => {
  handleTableDataResult();
  filterVisible.value = false;
};

</script>

<style scoped>
.input-with-select .el-input-group__prepend {
  background-color: var(--el-fill-color-blank);
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

