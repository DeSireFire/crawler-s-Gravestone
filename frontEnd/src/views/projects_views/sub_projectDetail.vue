<!-- sub_workerLinks.vue -->
<template>
  <div>
    <div class="plugins-tips">
      <b>项目首页</b>:
      <el-tag class="ml-2" type="success">{{ params_info.name }}</el-tag>
    </div>
    <el-row>
      <el-col :span="11">
        <div>
          <el-form ref="formRef" :rules="rules" :model="params_info" label-width="80px">
            <el-form-item label="项目编号" prop="pid">
              <el-input v-model="params_info.pid" :disabled="true"></el-input>
            </el-form-item>
            <el-form-item label="项目名称" prop="nickname">
              <el-input v-model="params_info.nickname" :disabled="true"></el-input>
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
            <el-form-item label="原始名称" prop="name">
              <el-input v-model="params_info.name" :disabled="true"></el-input>
            </el-form-item>
            <el-form-item label="所属用户" prop="author">
              <el-input v-model="params_info.author" :disabled="true"></el-input>
            </el-form-item>
            <el-form-item label="更新时间" prop="update_time">
              <el-input v-model="params_info.update_time" :disabled="true"></el-input>
            </el-form-item>
          </el-form>
        </div>
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
  </div>
</template>

<script setup lang="ts" name="sub_projectDetail">
import {ref, reactive, onBeforeMount, onMounted, watch} from 'vue';
import {ElMessage, ElMessageBox, FormInstance, FormRules} from 'element-plus';
import { getProject,getPTask } from '~/api/projects';
import {Delete, Edit, Plus, Refresh} from '@element-plus/icons-vue';
import {fetchChartss} from "~/api";
import * as echarts from "echarts";
import {useRoute} from "vue-router";
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
// 声明 props
const props = defineProps<{
  pid: string;
}>();
const pid = ref(props.pid||'');
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

// 刷新数据
const handleFlush = async (init = true) => {
  // // 获取pid
  pid.value = props.pid ?? ""
  if (!pid.value) {
    console.log('页面刷新，判断')
    handleProjectInfo();
  }

  if (pid.value) {
    // 获取数据
    const res = (await getProject({
      pid: pid.value
    }))

    // params_info.id = res.data.id
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

// 获取当前路由
const route = useRoute();
// 监听路由参数的变化
watch(() => props.pid, (newPid, oldPid) => {
  pid.value = newPid;
  handleFlush();
});

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

// 在子页面加载时获取并更新数据
// onMounted(() => {
//   // 根据 props.pid 进行数据请求并更新 params_info
//   pid.value = props.pid
//   console.log(2333)
//   console.log(pid.value)
// // 打开页面就刷新
//   handleFlush();
// });

// onBeforeMount(() => {
//   // getPTaskDatas()
//   initEcharts()
// })

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

