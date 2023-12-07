<template>
  <div class="container">
    <div class="plugins-tips">
      <b>知识星球-文档分享</b>
    </div>
    <el-row>
      <el-col :span="12">
        <div class="custom-card">
          <!-- 左侧图片 -->
          <div class="card-image">
            <img src="https://p8.itc.cn/images01/20210124/ec2752da99f44008896fde69f3eb921d.jpeg" alt="Image">
          </div>

          <!-- 右侧文字内容 -->
          <div class="card-text">
            <h3>Title</h3>
            <p class="desc">
              分层架构是一种将系统划分为多个层次的设计模式，每个层次专注于特定的功能。这样的设计使得系统的不同部分能够更好地组织和管理，从而提高了系统的可维护性、可扩展性和可理解性。
            </p>
            <el-divider />
            <p class="author-time">
              <span>Author: John Doe</span> | <span>Published on: January 1, 2023</span>
            </p>
          </div>
        </div>
      </el-col>
      <el-col :span="12">
        <div class="custom-card">
          <!-- 左侧图片 -->
          <div class="card-image">
            <img src="https://p8.itc.cn/images01/20210124/ec2752da99f44008896fde69f3eb921d.jpeg" alt="Image">
          </div>

          <!-- 右侧文字内容 -->
          <div class="card-text">
            <h3>Title</h3>
            <p class="desc">
              分层架构是一种将系统划分为多个层次的设计模式，每个层次专注于特定的功能。这样的设计使得系统的不同部分能够更好地组织和管理，从而提高了系统的可维护性、可扩展性和可理解性。
            </p>
            <el-divider />
            <p class="author-time">
              <span>Author: John Doe</span> | <span>Published on: January 1, 2023</span>
            </p>
          </div>
        </div>
      </el-col>
    </el-row>

  </div>
</template>

<script setup lang="ts" name="docs_shape">
import { ref, reactive } from 'vue';
const currentDate = ref(new Date())
</script>

<style>
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
.card-image {
  flex: 1;
  overflow: hidden;
  border-top-left-radius: 15px;
  border-bottom-left-radius: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover; /* 图片填充方式，保持纵横比并垂直水平居中 */
}

/* 右侧文字内容样式 */
.card-text {
  flex: 2;
  padding: 20px;
  display: flex;
  flex-direction: column; /* 设置为列布局，让内容垂直排列 */
  justify-content: space-between; /* 垂直方向上两端对齐 */
  height: 100%; /* 让 .card-text 撑满整个高度 */
}

.card-text h3 {
  margin-bottom: 10px;
  color: #333;
}

.card-text .desc{
  margin: 0; /* 清除段落默认的上下边距 */
  max-height: 70px; /* 摘要最大高度为卡片高度的50% */
  overflow: hidden; /* 超出部分隐藏 */
  text-overflow: ellipsis; /* 超出部分显示省略号 */
}

.card-text p {
  color: #666;
}

.card-text .author-time {
  color: #888;
  margin-top: auto; /* 将作者和发布时间推到底部 */
}

</style>
