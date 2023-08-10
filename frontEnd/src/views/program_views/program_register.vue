<template>
  <div>
    <el-row>
      <el-col :span="24">
        <el-card shadow="hover" class="mgb20">
          <div class="plugins-tips">
            <b>程序登记</b>
          </div>
          <div class="user-info">
            <p>用于登记注册常用程序，便于日后托管运行使用。</p>
            <p>
            程序运行支持：
              Python ✔
            </p>
          </div>
          <el-button type="primary" :icon="Plus" @click="addVisible = true">新增程序</el-button>
        </el-card>
      </el-col>
    </el-row>
    <el-row :gutter="20" v-if="programs_body.programs.length > 0">
      <el-col :span="6" v-for="program in programs_body.programs">
        <el-card shadow="hover" style="height: 267px">
          <template #header>
            <div class="clearfix">
              <span>{{ program.name }}</span>
            </div>
          </template>
          <div class="card-content">
            <el-form
                label-position="right"
                label-width="50px"
                :model="program"
                size="small"
            >
              <el-form-item label="程序名">
                <el-input v-model="program.name" disabled/>
              </el-form-item>
              <el-form-item label="备注">
                <el-input v-model="program.description" disabled/>
              </el-form-item>
              <el-form-item label="Git">
                <el-input v-model="program.git_repo" disabled/>
              </el-form-item>
              <el-form-item label="路径">
                <el-input v-model="program.repo_path" disabled/>
              </el-form-item>
            </el-form>
          </div>
          <div class="card-footer">
            <el-button type="primary" text>
              详情
            </el-button>
            <el-button type="danger" text>
              删除
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
    <el-row :gutter="20" v-else>
      <el-col :span="24">
        <div class="container">
          <p style="color:#606266">尚未添加任何程序...</p>
        </div>
      </el-col>
    </el-row>

    <!-- 弹出框 -->
    <el-dialog title="登记程序" v-model="addVisible" width="40%">
      <el-form label-width="80px">
        <el-form-item label="程序名称">
          <el-input v-model="addForm.name"></el-input>
        </el-form-item>
        <el-form-item label="Git地址">
          <el-input v-model="addForm.git_repo"></el-input>
        </el-form-item>
        <el-form-item label="执行路径">
          <el-input v-model="addForm.git_repo" placeholder="./"></el-input>
        </el-form-item>
        <el-form-item label="运行文件">
          <el-input type="textarea" v-model="addForm.shell" placeholder="用来启动python程序的文件"></el-input>
        </el-form-item>
        <el-form-item label="依赖文件">
          <el-input v-model="addForm.requirements" placeholder="./requirements.text"></el-input>
        </el-form-item>
        <el-form-item label="执行环境">
          <el-input v-model="addForm.interpreter" placeholder="需要进入的依赖环境地址如:./venv"></el-input>
        </el-form-item>
        <el-form-item label="登记方/人">
          <el-input v-model="addForm.author"></el-input>
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="addForm.description"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
				<span class="dialog-footer">
					<el-button @click="addVisible = false">取 消</el-button>
					<el-button type="primary" @click="addSaveEdit">确 定</el-button>
				</span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts" name="program_register">
import {onBeforeMount, reactive, ref} from 'vue';
import {Delete, Edit, Search, Plus} from '@element-plus/icons-vue';
import {getPrograms, addPrograms, delPrograms, getProgram} from "~/api/programs";
import {ElMessage} from "element-plus";

interface TableItem {
  id: string;
  cid: string;
  name: string;
  git_repo: string;
  base_path: string;
  repo_path: string;
  shell: string;
  requirements: string;
  interpreter: string;
  description: string;
  author: string;
  extra: string;
  create_time: string;
  update_time: string;
}

const programs_body = reactive({
  programs: [],
})

// 刷新数据
const handleFlush = async (init = true) => {
  // 获取数据列表
  const res = (await getPrograms())
  if (res.isSuccess) {
    programs_body.programs = res.data.list || []
  } else {
    ElMessage.warning(`未获取到已注册的程序！`);
  }
};

// 新增数据
const addForm = reactive({
  name: '',
  git_repo: '',
  base_path: '',
  repo_path: '',
  shell: '',
  requirements: '',
  interpreter: '',
  description: '',
  author: '',
})
const addVisible = ref(false);
// const handleAdd = () => {
//   addVisible.value = true;
// };
const addSaveEdit = async () => {
  addForm.author = localStorage.getItem('ms_username') as string;
  // 向后端发起操作
  const response = (await addPrograms(addForm));
  if (response.isSuccess) {
    addVisible.value = false;
    handleFlush();
    ElMessage.success(`新增 ${addForm.name} 成功！`);
  } else {
    ElMessage.error(`新增 ${addForm.name} 失败！`);
  }
};

onBeforeMount(() => {
  // 打开页面就刷新
  handleFlush();
})
</script>

<style scoped>
.card-container {
  max-height: 300px;
  overflow: hidden;
}
.card-content .el-form-item{
  margin-bottom: 5px;
}
.card-header {
  background-color: #f0f0f0;
  padding: 10px;
}

.card-content {
  padding-bottom: 20px;
  border-bottom: 2px solid #ccc;
}

.card-footer {
  padding: 10px;
}


/* 原始样式 */
.el-row {
  margin-bottom: 20px;
}

.grid-content {
  display: flex;
  align-items: center;
  height: 100px;
}

.grid-cont-right {
  flex: 1;
  text-align: center;
  font-size: 14px;
  color: #999;
}

.grid-num {
  font-size: 30px;
  font-weight: bold;
}

.grid-con-icon {
  font-size: 50px;
  width: 100px;
  height: 100px;
  text-align: center;
  line-height: 100px;
  color: #fff;
}

.grid-con-1 .grid-con-icon {
  background: rgb(45, 140, 240);
}

.grid-con-1 .grid-num {
  color: rgb(45, 140, 240);
}

.grid-con-2 .grid-con-icon {
  background: rgb(100, 213, 114);
}

.grid-con-2 .grid-num {
  color: rgb(100, 213, 114);
}

.grid-con-3 .grid-con-icon {
  background: rgb(242, 94, 67);
}

.grid-con-3 .grid-num {
  color: rgb(242, 94, 67);
}

.user-info {
  display: flex;
  align-items: center;
  padding-bottom: 20px;
  border-bottom: 2px solid #ccc;
  margin-bottom: 20px;
}

.user-info-cont {
  padding-left: 50px;
  flex: 1;
  font-size: 14px;
  color: #999;
}

.user-info-cont div:first-child {
  font-size: 30px;
  color: #222;
}

.user-info-list {
  font-size: 14px;
  color: #999;
  line-height: 25px;
}

.user-info-list span {
  margin-left: 70px;
}

.mgb20 {
  margin-bottom: 20px;
}

.todo-item {
  font-size: 14px;
}

.todo-item-del {
  text-decoration: line-through;
  color: #999;
}

.schart {
  width: 100%;
  height: 300px;
}
</style>
