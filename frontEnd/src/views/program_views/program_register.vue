<template>
  <div>
    <el-row>
      <el-col :span="24">
        <el-card shadow="hover" class="mgb20">
          <div class="plugins-tips">
            <b>程序登记</b>
          </div>
          <div class="user-info">
            <p>用于登记注册常用程序，便于日后托管使用。</p>
<!--            <p>-->
<!--              程序运行支持：-->
<!--              Python ✔-->
<!--            </p>-->
          </div>
          <el-button type="primary" :icon="Plus" @click="addVisible = true">新增程序</el-button>
          <el-button type="primary" :icon="Refresh" @click="handleFlush">刷新列表</el-button>
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
            <el-button type="primary" text @click="handleInfo(program)">
              详情
            </el-button>
            <el-button type="primary" text @click="handleEdit(program)">
              修改
            </el-button>
            <el-button type="danger" text @click="handleDelete(program)">
              删除
            </el-button>
            <el-button type="danger" text >
              占位
            </el-button>
            <el-button type="danger" text >
              占位
            </el-button>
            <el-button type="danger" text >
              占位
            </el-button>
<!--            <el-button type="primary" text @click="actionVisible = true">-->
<!--              操作-->
<!--            </el-button>-->
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
          <el-input v-model="addForm.repo_path" placeholder="./"></el-input>
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

    <el-dialog title="详细信息" v-model="infoVisible" width="40%">
      <el-form label-width="100px">
        <el-form-item class="el-form-item-compact" v-for="(value, key) in infoForm"
                      :key="key" :label="keyNames[key]+':'">
          <el-input v-model="infoForm[key]" disabled/>
        </el-form-item>
      </el-form>
      <template #footer>
				<span class="dialog-footer">
					<el-button @click="infoVisible = false">关闭</el-button>
				</span>
      </template>
    </el-dialog>

    <el-dialog title="信息编辑" v-model="editVisible" width="40%">
      <el-form label-width="100px">
        <!--用来前端渲染的字段-->
        <el-form-item class="el-form-item-compact" v-for="(value, key) in addForm"
                      :key="key" :label="keyNames[key]+':'">
          <el-input v-model="editForm[key]"/>
        </el-form-item>

      </el-form>
      <template #footer>
				<span class="dialog-footer">
					<el-button @click="editVisible = false">取 消</el-button>
					<el-button type="primary" @click="editSaveEdit">提 交</el-button>
				</span>
      </template>
    </el-dialog>

    <el-dialog title="程序操作" v-model="actionVisible" width="40%">
      <el-form label-width="100px">
        <el-form-item class="el-form-item-compact" v-for="(value, key) in infoForm"
                      :key="key" :label="keyNames[key]+':'">
          <el-input v-model="infoForm[key]" disabled/>
        </el-form-item>
      </el-form>
      <template #footer>
				<span class="dialog-footer">
					<el-button @click="infoVisible = false">关闭</el-button>
				</span>
      </template>
    </el-dialog>
  </div>
</template>
<script setup lang="ts" name="program_register">
import {onBeforeMount, reactive, ref} from 'vue';
import {ElMessage, ElMessageBox} from "element-plus";
import {getPrograms, addPrograms, delPrograms, getProgram, updatePrograms} from "~/api/programs";
import {Delete, Edit, Search, Plus, Refresh} from '@element-plus/icons-vue';
import {ElText} from 'element-plus';

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

// 字段名称对照
const keyNames = reactive({
  id: '编号',
  cid: '程序号',
  name: '程序名',
  git_repo: 'Git地址',
  base_path: '程序路径',
  repo_path: '启动路径',
  shell: 'Shel命令',
  requirements: '依赖名单',
  interpreter: '执行环境',
  description: '备注',
  author: '登记方/人',
  extra: '附加信息',
  create_time: '创建时间',
  update_time: '更新时间',
})
// 添加更多需要禁止输入的字段名
const disabledFields = reactive(['id', 'cid', 'name']);
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
  repo_path: '',
  base_path: '',
  shell: '',
  requirements: '',
  interpreter: '',
  description: '',
  author: '',
})
const addVisible = ref(false);
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

// 详细信息查看
const infoVisible = ref(false);
const infoForm = reactive({
  cid: '',
  name: '',
  git_repo: '',
  repo_path: '',
  base_path: '',
  shell: '',
  requirements: '',
  interpreter: '',
  description: '',
  author: '',
})
const handleInfo = (program: any) => {
  console.log("program", program)
  infoForm.cid = program.cid;
  infoForm.name = program.name;
  infoForm.git_repo = program.git_repo;
  infoForm.repo_path = program.repo_path;
  infoForm.base_path = program.base_path;
  infoForm.shell = program.shell;
  infoForm.requirements = program.requirements;
  infoForm.interpreter = program.interpreter;
  infoForm.description = program.description;
  infoForm.author = program.author;
  infoVisible.value = true;
};

// 修改操作,表格编辑时弹窗和保存
const editVisible = ref(false);
const editForm = reactive({
  id: '',
  cid: '',
  name: '',
  git_repo: '',
  repo_path: '',
  base_path: '',
  shell: '',
  requirements: '',
  interpreter: '',
  description: '',
  author: '',
});
const handleEdit = (program: any) => {
  editForm.id = program.id;
  editForm.cid = program.cid;
  editForm.name = program.name;
  editForm.git_repo = program.git_repo;
  editForm.repo_path = program.repo_path;
  editForm.base_path = program.base_path;
  editForm.shell = program.shell;
  editForm.requirements = program.requirements;
  editForm.interpreter = program.interpreter;
  editForm.description = program.description;
  editForm.author = program.author;
  editVisible.value = true;
};
const editSaveEdit = async () => {
  // 向后端发起操作
  const response = (await updatePrograms(editForm));
  if (response.isSuccess) {
    handleFlush();
    ElMessage.success(`修改 ${editForm.name} 成功！`);
  } else {
    ElMessage.error(`修改 ${editForm.name} 失败！`);
  }
  editVisible.value = false;
};

// 删除操作
const delform = reactive({
  cid: '',
  name: '',
});
const handleDelete = (program: any) => {
  // 二次确认删除
  ElMessageBox.confirm('确定要删除吗？', '提示', {
    type: 'warning'
  })
      .then(async () => { /* 处理正常时 */
        // 获取当前表行数据
        delform.cid = program.cid;
        delform.name = program.name;
        // 向后端发起删除操作
        const response = (await delPrograms(delform));
        if (response.isSuccess) {
          // 响应删除成功则弹出提示
          ElMessage.success('删除成功！');
          // 刷新缓存数据
          handleFlush();
        } else {
          // 响应删除失败则弹出错误
          throw new Error(response.errMsg);
        }
      })
      .catch((error) => { /* 处理失败时 */
        ElMessage.error(`删除失败! ${error}`);
      });

};

// 部署操作
const actionVisible=ref(false);

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

.card-content .el-form-item {
  margin-bottom: 5px;
}

.el-form-item-compact {
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
/*.el-row {*/
/*  margin-bottom: 20px;*/
/*}*/

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
