<template>
  <div class="container">
    <div>
      <iframe v-if="reportType==0" name = "child" id = "child" v-bind:src="reportUrl"
              width="auto" height="300"
              frameborder="0" scrolling="no"  style="position:absolute;top:80px;left: 30px;"
      ></iframe>

      <div v-if="reportType==1" v-html="htmlContent"
           width="auto" height="300"  scrolling="no"  style="position:absolute;top:80px;left: 30px;"></div>

    </div>
  </div>
</template>

<script setup lang="ts" name="api_docs" frameborder="0" scrolling="no" width="100%"></script>

<script>
// import {
//   getFile
// } from '@/api/report'
export default {
  mounted() {
    /**
     * iframe-宽高自适应显示
     */
    function changeMobsfIframe() {
      const mobsf = document.getElementById('child')
      const deviceWidth = document.body.clientWidth
      const deviceHeight = document.body.clientHeight
      mobsf.style.width = (Number(deviceWidth) - 30) + 'px' // 数字是页面布局宽度差值
      mobsf.style.height = (Number(deviceHeight) - 80) + 'px' // 数字是页面布局高度差
    }

    changeMobsfIframe()

    window.onresize = function() {
      changeMobsfIframe()
    }
  },

  data() {
    return {
      htmlContent: '',
      reportUrl: 'http://localhost:50830/docs',
      reportType: ''
    }
  },
  created() {
    // this.fileName = '../static/file/' + this.$route.params.report_url
    this.reportUrl = this.$route.params.reportUrl
    this.reportType = this.$route.params.reportType
  }
}
</script>

<style>

</style>
