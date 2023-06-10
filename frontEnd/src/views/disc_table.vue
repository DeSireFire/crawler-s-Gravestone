<template>
  <div class="container">
    <div class="plugins-tips">
      vue-echart：vue.js封装sChart.js的图表组件。 访问地址：
    </div>
    <el-row ref="chartsDatas" :gutter="20" v-for="(item,index) in chartsDatas" :key="index">
      <el-col :span="16">
        <el-card shadow="hover">
          <div :id="`chart${index}`" class="echart" :options="schartOption"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts"  name="basecharts">
import { onBeforeMount, reactive, ref, onMounted, onUpdated } from 'vue'
import * as echarts from 'echarts'
import {fetchCharts,fetchChartss} from '../../src/api';
import { defineComponent } from 'vue'
const chartsDatas = ref(null)
interface schartOption {
  schartOption: any;
}

const schartOption: schartOption = {
  schartOption: {}
};



// 获取数据
const getDatas = async () => {
  chartsDatas.value = (await fetchChartss()).data
  return chartsDatas.value
}

// 渲染图表
const initEcharts = async () => {
  const temps = (await fetchChartss()).data
  console.log("temps.value",temps)
  temps.forEach((item: any, index: string | number) => {
    let schartOption  = temps[index]
    let element = document.getElementById(`chart${index}`)
    if (element){
      let mainEchart = echarts.init(element)
      mainEchart.setOption(schartOption,{notMerge:true})
    }
  });
}

onBeforeMount(() => {
  // getDatas()
})

onMounted(() => {
  // console.log("chartsDatas",chartsDatas)
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
