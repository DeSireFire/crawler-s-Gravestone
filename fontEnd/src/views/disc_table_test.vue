<template>
  <div class="container">
    <div class="plugins-tips">
      vue-echart：vue.js封装sChart.js的图表组件。 访问地址：
    </div>
    <el-row ref="chartsDatas" :gutter="20" v-for="(item,index) in chartsDatas" :key="index">
      <el-col :span="16">
        <el-card shadow="hover">
          <div :id="`chart${index}`" class="echart" :options="item">{{item}}</div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts"  name="basecharts">
import { nextTick, reactive, ref, onBeforeMount, onMounted, onUpdated} from 'vue'
import * as echarts from 'echarts'
import {fetchCharts,fetchChartss} from '../../src/api';
// const chartList = [1,2,3,4,5]
// const chartsDatas = (await fetchChartss()).data
const chartsDatas = ref(null)

const getDatas = async () => {
  chartsDatas.value = (await fetchChartss()).data
}

// const initEcharts = async () => {
//   const temps = chartsDatas.value
//   temps.forEach((item, index) => {
//     let option = temps[index]
//     let mainEchart = echarts.init(document.getElementById(`chart${index}`))
//     mainEchart.setOption(option)
//   });
// }

onBeforeMount(() => {
  getDatas()
  console.log(chartsDatas.value)
  // initEcharts()
})
onMounted(() => {
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
.container {
  min-height: 100%;
  min-width: auto;
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
