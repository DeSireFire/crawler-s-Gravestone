<template>
  <div class="container">
    <div ref="vecharts" class="echart" :options="option"></div>
  </div>
</template>

<script setup lang="ts"  name="basecharts">
import { reactive, ref, onMounted } from 'vue'
import * as echarts from 'echarts'
import {fetchCharts} from '../api/index';
const vecharts = ref(null)
let option = ref({})

// 获取表格数据
const getData = async () => {
  fetchCharts().then(res => {
    option.value = res.data;
    initEcgarts();
  });
};

const initEcgarts = () => {
  const mainEchart = echarts.init(vecharts.value)
  console.log("option==>",option)
  console.log("option.value==>",option.value)
  mainEchart.setOption(option.value)
}

onMounted(() => {
  getData();
})
</script>

<style scoped>
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
</style>
