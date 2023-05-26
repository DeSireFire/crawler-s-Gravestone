<template>
  <div class="container">
    <div class="plugins-tips">
      vue-schart：vue.js封装sChart.js的图表组件。 访问地址：
      <a href="https://github.com/lin-xin/vue-schart" target="_blank">vue-schart</a>
    </div>
    <div class="schart-box">
      <div class="content-title">折线图</div>
      <schart class="schart" canvasId="line" :options="datas"></schart>
    </div>
  </div>
</template>

<script setup lang="ts" name="basecharts">
import { ref } from 'vue';
import Schart from 'vue-schart';
import {fetchdisc} from '../../src/api';
const datas = ref({});

// 获取表格数据
const getData = () => {
  fetchdisc().then(res => {
    datas.value = res.data;
  });
};
getData();

// const getData = async () => {
//   const res = await fetchdisc();
//   console.log("res========>",res)
//   datas.value = await res.data;
// };
// getData();
console.log("data========>",datas)

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
.content-title {
  clear: both;
  font-weight: 400;
  line-height: 50px;
  margin: 10px 0;
  font-size: 22px;
  color: #1f2f3d;
}
</style>
