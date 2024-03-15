<template>
  <div class="container">
    <h2>平台导航</h2>
    <p style="line-height: 50px">点击相应图标即可完成页面跳转：（共{{ iconList.length }}个图标）</p>
    <br />
    <div class="search-box">
      <el-input class="search" size="large" v-model="keyword" clearable placeholder="需要搜索的网站关键字"></el-input>
    </div>
    <ul>
      <li class="icon-li" v-for="(item, index) in filteredList" :key="index">
        <div class="icon-li-content" @click="goToUrl(item.url)">
          <i :class="`el-icon-lx-${item.icon}`"></i>
          <span>{{ item.name }}</span>
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts" name="icon">
import { computed, ref } from 'vue';

// 修改数据结构为数组嵌套对象
const iconList: Array<{ name: string; url: string; icon: string }> = [
  { name: '尚书台', url: 'http://shangshutai.sinohealth.cn/#/home', icon: 'tag' },
  { name: '天宫数智平台', url: 'http://dp.sinohealth.cn/#/', icon: 'tag' },
  { name: '运维工单系统', url: 'http://yunwei.sinohealth.cn/', icon: 'tag' },
  { name: '主数据海豚调度', url: 'http://192.168.60.122:7070/dolphinscheduler/ui/#/home', icon: 'tag' },
];

const keyword = ref('');
// 使用计算属性过滤列表
const filteredList = computed(() => {
  return iconList.filter(item => {
    return item.name.indexOf(keyword.value) !== -1 || item.url.indexOf(keyword.value) !== -1;
  });
});

// 添加方法用于跳转外部URL
function goToUrl(url: string) {
  window.location.href = url;
}
</script>

<style scoped>
.search-box {
  text-align: center;
  margin-top: 10px;
}
.search {
  width: 300px;
}
ul,
li {
  list-style: none;
}
.icon-li {
  display: inline-block;
  padding: 10px;
  width: 120px;
  height: 120px;
}
.icon-li-content {
  display: flex;
  height: 100%;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}
.icon-li-content i {
  font-size: 36px;
  color: #606266;
}
.icon-li-content span {
  margin-top: 10px;
  color: #787878;
}
</style>
