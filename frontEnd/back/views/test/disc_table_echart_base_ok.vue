<template>
  <div class="container">
    <div ref="vecharts" class="echart"></div>
  </div>
</template>

<script setup lang="ts"  name="basecharts">
import { reactive, ref, onMounted } from 'vue'
import * as echarts from 'echarts'
import {fetchCharts} from '../../src/api';
const vecharts = ref()
onMounted(() => {
  initEcgarts()
})
// const option = ref({})
// // 获取表格数据
// const getData = () => {
//   fetchCharts().then(res => {
//     console.log("res",res)
//     console.log("res.data",res.data)
//     option.value = res.data
//     // return res.data;
//   });
// };
// getData();

const initEcgarts = () => {
  const mainEchart = echarts.init(vecharts.value)
  let option = {
    title: {
      text: "数据统计",
    },
    tooltip: {
      trigger: "axis",
    },
    legend: {
      data: ["Email", "Union Ads", "Video Ads", "Direct", "Search Engine"],
    },
    grid: {
      left: "3%",
      right: "4%",
      bottom: "3%",
      containLabel: true,
    },
    toolbox: {
      feature: {
        saveAsImage: {},
      },
    },
    xAxis: {
      type: "category",
      boundaryGap: false,
      data: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    },
    yAxis: {
      type: "value",
    },
    series: [
      {
        name: "Email",
        type: "line",
        stack: "Total",
        data: [120, 132, 101, 134, 90, 230, 210],
      },
      {
        name: "Union Ads",
        type: "line",
        stack: "Total",
        data: [220, 182, 191, 234, 290, 330, 310],
      },
      {
        name: "Video Ads",
        type: "line",
        stack: "Total",
        data: [150, 232, 201, 154, 190, 330, 410],
      },
      {
        name: "Direct",
        type: "line",
        stack: "Total",
        data: [320, 332, 301, 334, 390, 330, 320],
      },
      {
        name: "Search Engine",
        type: "line",
        stack: "Total",
        data: [820, 932, 901, 934, 1290, 1330, 1320],
      },
    ],
  };
  mainEchart.setOption(option)
}
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
