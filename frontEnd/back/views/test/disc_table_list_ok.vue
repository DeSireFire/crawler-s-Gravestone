<template>
  <div class="container">
    <div class="plugins-tips">
      vue-echart：vue.js封装sChart.js的图表组件。 访问地址：
    </div>
    <el-row :gutter="20" v-for="(item,index) in chartList" :key="index">
      <el-col :span="16">
        <el-card shadow="hover">
          <div :id="`chart${index}`" class="echart" :options="option"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts"  name="basecharts">
import { nextTick, reactive, ref, onMounted } from 'vue'
import * as echarts from 'echarts'
import {fetchCharts,fetchChartss} from '../../src/api';

const chartList = [1,2,3,4,5]
const initEcharts = async () => {
  const chartsDatas = (await fetchChartss()).data

  // const chartList = [];
  // chartsDatas.forEach((item, index) => {
  //   console.log(index+1)
  //   chartList.push(index+1)
  // });

  chartsDatas.forEach((item, index) => {
    let option = chartsDatas[index]
    let mainEchart = echarts.init(document.getElementById(`chart${index}`))
    // let mainEchart = echarts.init(document.getElementsByClassName(`echart`))
    mainEchart.setOption(option)
  });

}
onMounted(() => {
  initEcharts()
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
