<template>
  <div class="container">
    <el-row :gutter="20">
      <el-col :span="12">
        <el-card shadow="hover">
          <div v-for="(item, i) in users" :key="i">索引：{{i}} 内容：{{item}}</div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts"  name="basecharts">
import { reactive, ref, onMounted } from 'vue'
import * as echarts from 'echarts'
import {fetchCharts} from '../../src/api';
const vechart1 = ref(null)
const vechart2 = ref(null)
let option1 = ref({})
let option2 = ref({})
const users = [1,2,3,4,5]
const initEcgarts = async () => {
  option1.value = (await fetchCharts()).data
  option2.value = (await fetchCharts()).data
  const mainEchart1 = echarts.init(vechart1.value)
  const mainEchart2 = echarts.init(vechart2.value)
  mainEchart1.setOption(option1.value)
  mainEchart2.setOption(option2.value)
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
