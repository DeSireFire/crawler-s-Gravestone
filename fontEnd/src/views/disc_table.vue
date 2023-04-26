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
const initEcgarts = async () => {
  option.value = (await fetchCharts()).data
  const mainEchart = echarts.init(vecharts.value)
  mainEchart.setOption(option.value)
}

onMounted(() => {
  initEcgarts()
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
