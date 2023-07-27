<!-- sub_workerLinks.vue -->
<template>
  <div class="plugins-tips">项目首页</div>
  <el-row>
    <el-col :span="11">
      <div>
        <el-form ref="formRef" :rules="rules" :model="params_info" label-width="80px">
          <el-form-item label="项目编号" prop="pid">
            <el-input v-model="params_info.pid" :disabled="true"></el-input>
          </el-form-item>
          <el-form-item label="项目名称" prop="name">
            <el-input v-model="params_info.name" :disabled="true"></el-input>
          </el-form-item>
          <el-form-item label="创建时间" prop="create_time">
            <el-input v-model="params_info.create_time" :disabled="true"></el-input>
          </el-form-item>
        </el-form>
      </div>
    </el-col>
    <el-col :span="1"></el-col>
    <el-col :span="11">
      <div>
        <el-form ref="formRef" :rules="rules" :model="params_info" label-width="80px">
          <el-form-item label="项目备注" prop="nickname">
            <el-input v-model="params_info.nickname" :disabled="true"></el-input>
          </el-form-item>
          <el-form-item label="所属用户" prop="author">
            <el-input v-model="params_info.author" :disabled="true"></el-input>
          </el-form-item>
          <el-form-item label="更新时间" prop="update_time">
            <el-input v-model="params_info.update_time" :disabled="true"></el-input>
          </el-form-item>
        </el-form>
      </div>
      <!--      <el-table :data="state.unread" :show-header="false" style="width: 100%">-->
      <!--        <el-table-column>-->
      <!--          <template #default="scope">-->
      <!--            <span class="message-title">{{ scope.row.title }}</span>-->
      <!--          </template>-->
      <!--        </el-table-column>-->
      <!--        <el-table-column prop="date" width="180"></el-table-column>-->
      <!--        <el-table-column width="120">-->
      <!--          <template #default="scope">-->
      <!--            <el-button size="small" @click="handleRead(scope.$index)">标为已读</el-button>-->
      <!--          </template>-->
      <!--        </el-table-column>-->
      <!--      </el-table>-->
    </el-col>
    <el-col :span="1"></el-col>
  </el-row>
  <el-row>
    <el-col :span="23">
      <div>
        <el-form ref="formRef" :rules="rules" :model="params_info" label-width="80px">
          <el-form-item label="背景描述" prop="description">
            <el-input type="textarea" rows="5" v-model="params_info.description" :disabled="true"></el-input>
          </el-form-item>
        </el-form>
      </div>
    </el-col>
    <el-col :span="1"></el-col>
  </el-row>
  <div class="handle-row">
    <el-button type="primary" @click="$router.push('/projects_list')">
      返回项目列表
    </el-button>
  </div>
  <el-divider></el-divider>
  <el-row ref="chartsDatas" :gutter="20" v-for="(item,index) in chartsDatas" :key="index">
    <el-col :span="16">
      <el-card shadow="hover">
        <div :id="`chart${index}`" class="echart" :options="schartOption"></div>
      </el-card>
    </el-col>
  </el-row>
</template>

<script setup lang="ts" name="sub_projectDetail">
import {ref, reactive, onBeforeMount, onMounted} from 'vue';
import {ElMessage, ElMessageBox, FormInstance, FormRules} from 'element-plus';
import { getProject,getPTask } from '~/api/projects';
import {Delete, Edit, Plus, Refresh} from '@element-plus/icons-vue';
import {fetchChartss} from "~/api";
import * as echarts from "echarts";

const chartsDatas = ref(null)
const formRef = ref<FormInstance>();
const rules: FormRules = {
  pid: [{required: true, message: '项目唯一标识', trigger: 'blur'}],
  name: [{required: true, message: '项目名称不能为空，不能重复！', trigger: 'blur'}],
};
interface baseSchartOption {
  schartOption: any;
}

const schartOption: baseSchartOption = {
  schartOption: {}
};

const pid = ref('');
const params_info = reactive({
  id: "",
  pid: "",
  name: "",
  nickname: "",
  description: "",
  author: "",
  create_time: "",
  update_time: "",
});
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

// 获取数据
const getPTaskDatas = async () => {
  chartsDatas.value = (await getPTask()).data.list
}

// 渲染图表
const initEcharts = async () => {
  const res = (await getPTask()).data;
  const temps = res.list;
  console.log("temps.value", temps)
  temps.forEach((item: any, index: string | number) => {
    let schartOption = temps[index]
    let element = document.getElementById(`chart${index}`)
    if (element) {
      let mainEchart = echarts.init(element)
      mainEchart.setOption(schartOption, {notMerge: true})
    }
  });
}


onBeforeMount(() => {
  // getPTaskDatas()
  initEcharts()
})

//
// onMounted(() => {
//   // console.log("chartsDatas",chartsDatas)
//
// })

</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 100%;
}

.chart {
  width: 100%;
  height: calc(100% - 30px);
}

.schart-box {
  display: inline-block;
  margin: 20px;
}
.schart {
  width: 600px;
  height: 400px;
}
.echart {
  width: auto;
  height: 400px;
}
.content-title {
  clear: both;
  font-weight: 400;
  line-height: 50px;
  margin: 10px 0;
  font-size: 22px;
  color: #1f2f3d;
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
</style>

