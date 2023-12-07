<template>
  <div class="container">
    <div class="plugins-tips">
      <b>知识星球-文档分享</b>
    </div>

    <div class="handle-box">
      <el-input v-model="searchText" placeholder="搜索文章关键词.." class="handle-input mr10">
        <template #append>
          <el-button :icon="Search" @click="handleSearch()"/>
        </template>
      </el-input>
      <el-button type="primary" :icon="Refresh" @click="handleFlush()">刷新列表</el-button>
    </div>
    <el-divider/>
    <div v-if="!resData.value" class="container">
      <el-row>
        <el-col :span="12" v-for="(item, index) in resData" :key="index">
          <div class="custom-card" v-show="item">
            <!-- 左侧图片 -->
            <div class="card-image">
              <img src="https://p8.itc.cn/images01/20210124/ec2752da99f44008896fde69f3eb921d.jpeg" alt="Image">
            </div>
            <!-- 右侧文字内容 -->
            <div class="card-text">
              <div v-if="isSearch">
                <router-link :to="
                { path: '/docs_previwer', query: {
                  doc_id: item.doc_id,
                  author:item.author,
                  title:item.title
                }}">
                  <h3  v-html="highlightText(item.title)"></h3>
                </router-link>
                <p class="desc" v-html="highlightText(item.desc)"></p>
              </div>
              <div v-else class="no-data">
                <router-link :to="
                { path: '/docs_previwer', query: {
                  doc_id: item.doc_id,
                  author:item.author,
                  title:item.title
                }}">
                  <h3>{{item.title}}</h3>
                </router-link>

                <p class="desc">
                  {{item.desc}}
                </p>
              </div>
              <el-divider/>
              <p class="author-time">
                <span>作者: {{item.author || "无"}}</span> | <span>发布于: {{item.create_time}}</span>
              </p>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>
    <div v-else class="container">
      <h1 class="none-list">暂无分享文章...</h1>
    </div>
  </div>
</template>

<script setup lang="ts" name="docs_shape">
import {ref, reactive, onMounted, watchEffect } from 'vue';
import {getShape} from "~/api/docs";
import {ElMessage} from "element-plus";
import {Delete, Edit, Search, Plus, FullScreen, Close, RefreshRight, Refresh} from '@element-plus/icons-vue';
interface shapeItem {
  "title": string,
  "id": number,
  "author": string,
  "extra": string,
  "content": string,
  "md_content": string,
  "doc_id": string,
  "desc": string,
  "create_time": string,
}

const isSearch = ref(false); // 是否开启了搜索
const searchText = ref(''); // 搜索关键词
const rawData = ref<shapeItem[]>([]);  // 获取到的总数据
const resData = ref<shapeItem[]>([]);  // 展示用的数据
const filteredData = ref<shapeItem[]>([]); // 过滤后的数据

const get_shape_items = async () => {
  // 向后端发起操作
  const response = (await getShape());
  rawData.value = response.data.list.slice(0, response.data.list.length)
  if (response.isSuccess) {
    ElMessage.success(`文档分享刷新成功！`);
  } else {
    ElMessage.error(`文档分享刷新失败！`);
  }
  return rawData.value
};

// 处理数据刷新
const handleFlush = async () => {
  // 在这里替换成实际的后台数据请求
  resData.value = await get_shape_items();
  // 初始化搜索条件
  searchText.value = ''
  isSearch.value = false
  console.log(rawData.value)
};

// 处理数据搜索
const handleSearch = async () => {
  if (!searchText) {
    resData.value = rawData.value
    console.log(rawData.value)
  } else {
    filterData();
    isSearch.value = true
    resData.value = filteredData.value
    console.log("filteredData.value",filteredData.value)
    console.log("resData.value",resData.value)
  }
};

// 过滤数据函数
const filterData = () =>  {
  const keyword = searchText.value.toLowerCase();
  filteredData.value = rawData.value.filter(item =>
      (item.title && item.title.toLowerCase().includes(keyword)) ||
      (item.desc && item.desc.toLowerCase().includes(keyword)) ||
      (item.id && item.id.toString().includes(keyword)) ||
      (item.author && item.author.toLowerCase().includes(keyword))
  );
}

// 高亮匹配到的关键词
function highlightText(text: string): string {
  if (!text || !searchText.value || !isSearch.value) {
    return text;
  }
  const regex = new RegExp(`(${searchText.value})`, 'gi');
  return text.replace(regex, '<span class="highlight">$1</span>');
}


// 模拟从后台获取数据的过程
onMounted(async () => {
  handleFlush();
});
</script>

<style>
.none-list {
  padding: 32px;
  color: #6b778c;
  font-size: 32px;
  font-weight: 600;
}

.handle-input {
  width: 300px;
}
.handle-box {
  margin-bottom: 20px;
}
.mr10 {
  margin-right: 10px;
}
/* 卡片样式 */
.custom-card {
  display: flex;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin: 20px;
  background-color: #fff;
  max-height: 200px; /* 设置最大高度 */
  max-width: 100%; /* 设置最大宽度 */
}

/* 左侧图片样式 */
.custom-card .card-image {
  flex: 1;
  overflow: hidden;
  border-top-left-radius: 15px;
  border-bottom-left-radius: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.custom-card .card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover; /* 图片填充方式，保持纵横比并垂直水平居中 */
}

/* 右侧文字内容样式 */
.custom-card .card-text {
  flex: 2;
  padding: 20px;
  display: flex;
  flex-direction: column; /* 设置为列布局，让内容垂直排列 */
  justify-content: space-between; /* 垂直方向上两端对齐 */
  height: 100%; /* 让 .card-text 撑满整个高度 */
}

.custom-card .card-text h3 {
  margin-bottom: 10px;
  color: #333;
}

.custom-card .card-text .desc {
  margin: 0; /* 清除段落默认的上下边距 */
  height: 70px; /* 摘要最大高度为卡片高度的50% */
  overflow: hidden; /* 超出部分隐藏 */
  text-overflow: ellipsis; /* 超出部分显示省略号 */
}

.custom-card .card-text p {
  color: #666;
}

.custom-card .card-text .author-time {
  color: #888;
  margin-top: auto; /* 将作者和发布时间推到底部 */
}


/* 根据需要添加样式 */
.result-item {
  margin-bottom: 10px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

/* 添加高亮样式 */
.highlight {
  background-color: yellow;
  font-weight: bold;
}
</style>
