<template>
  <el-container>
    <el-header>Header</el-header>
    <el-main>
      <el-row>
        <el-col :span="12">
          <el-card>
            <el-button @click="showLog">Show Log</el-button>
            <el-dialog :visible.sync="dialogVisible" width="80%">
              <el-tabs v-model="activeTab">
                <el-tab-pane label="Log" name="log">
                  <pre>{{ log }}</pre>
                </el-tab-pane>
                <el-tab-pane label="JSON" name="json">
                  <pre>{{ json }}</pre>
                </el-tab-pane>
              </el-tabs>
            </el-dialog>
          </el-card>
        </el-col>
      </el-row>
    </el-main>
    <el-footer>Footer</el-footer>
  </el-container>
</template>

<script>
import { ref } from 'vue'
import { ElButton, ElCard, ElCol, ElContainer, ElDialog, ElFooter, ElHeader, ElMain, ElRow, ElTabPane, ElTabs } from 'element-plus'

export default {
  components: {
    [ElButton.name]: ElButton,
    [ElCard.name]: ElCard,
    [ElCol.name]: ElCol,
    [ElContainer.name]: ElContainer,
    [ElDialog.name]: ElDialog,
    [ElFooter.name]: ElFooter,
    [ElHeader.name]: ElHeader,
    [ElMain.name]: ElMain,
    [ElRow.name]: ElRow,
    [ElTabPane.name]: ElTabPane,
    [ElTabs.name]: ElTabs
  },
  setup () {
    const dialogVisible = ref(false)
    const activeTab = ref('log')
    const log = ref('')
    const json = ref('')

    function showLog () {
      dialogVisible.value = true
      log.value = 'This is a log message.'
      json.value = '{ "key": "value" }'
    }

    return {
      dialogVisible,
      activeTab,
      log,
      json,
      showLog
    }
  }
}

</script>
