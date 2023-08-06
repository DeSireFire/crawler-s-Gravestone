<template>
  <div> <!-- 元素包裹 -->
    <el-row :gutter="20">
      <el-col :span="24">
        <div class="container">
          <div class="plugins-tips">
            <b>警告设置</b>:
          </div>
          <el-tabs v-model="alarmers">
            <el-tab-pane :label="`电子邮件设置`" name="first">
              <div class="form-box">
                <el-form ref="formRefEmail" :rules="rulesEmail" :model="formEmail" label-width="100px">
                  <el-form-item label="告警名称" prop="name">
                    <el-input v-model="formEmail.name"></el-input>
                  </el-form-item>
                  <el-form-item label="推送邮箱" prop="email">
                    <el-input v-model="formEmail.email"></el-input>
                  </el-form-item>
                  <el-form-item label="告警类型" prop="resource" disabled>
                    <el-select v-model="formEmail.resource" placeholder="告警类型" disabled>
                      <el-option key="0" label="电子邮件" value="电子邮件"></el-option>
                      <el-option key="1" label="企微bot" value="企微bot"></el-option>
                    </el-select>
                  </el-form-item>
                  <el-form-item label="描述" prop="desc">
                    <el-input type="textarea" rows="5" v-model="formEmail.desc"></el-input>
                  </el-form-item>
                  <el-form-item>
                    <el-button type="primary" @click="submitEmailForm">表单提交</el-button>
                    <el-button @click="resetEmailForm">重置表单</el-button>
                  </el-form-item>
                </el-form>
              </div>
            </el-tab-pane>
            <el-tab-pane :label="`企微机器人设置`" name="second">
              <div class="form-box">
                <el-form ref="formRefQW" :rules="rulesQW" :model="formQW" label-width="100px">
                  <el-form-item label="告警名称" prop="name">
                    <el-input v-model="formQW.name"></el-input>
                  </el-form-item>
                  <el-form-item label="企微密钥" prop="qw_token">
                    <el-input v-model="formQW.qw_token"></el-input>
                  </el-form-item>
                  <el-form-item label="告警类型" prop="resource">
                    <el-select v-model="formQW.resource" placeholder="告警类型" disabled>
                      <el-option key="0" label="电子邮件" value="电子邮件"></el-option>
                      <el-option key="1" label="企微bot" value="企微bot"></el-option>
                    </el-select>
                  </el-form-item>
                  <el-form-item label="描述" prop="desc">
                    <el-input type="textarea" rows="5" v-model="formQW.desc"></el-input>
                  </el-form-item>
                  <el-form-item>
                    <el-button type="primary" @click="submitQWForm">表单提交</el-button>
                    <el-button @click="resetQWForm">重置表单</el-button>
                  </el-form-item>
                </el-form>
              </div>
            </el-tab-pane>
          </el-tabs>
        </div>
      </el-col>
    </el-row>
    <br/>
    <el-row :gutter="20">
      <el-col :span="24">
        <div class="container">
          <div class="plugins-tips">
            <b>电子邮件告警器</b>:
          </div>
          <el-table :data="filterEmail" :show-header="false" style="width: 100%">
            <el-table-column prop="name" :show-overflow-tooltip="true">
              <template #default="scope">
                <span class="message-title">名称: {{ scope.row.name }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="email" width="200" :show-overflow-tooltip="true">
              <template #default="scope">
                <span class="message-title">to: {{ scope.row.email }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="desc" width="200" :show-overflow-tooltip="true"></el-table-column>
            <el-table-column prop="create_time" width="180"></el-table-column>
            <el-table-column width="100">
              <template #default="scope">
                <el-button type="danger" @click="handleDel(scope.$index, scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-col>
    </el-row>
    <br/>
    <el-row :gutter="20">
      <el-col :span="24">
        <div class="container">
          <div class="plugins-tips">
            <b>企微bot告警器</b>:
          </div>
          <el-table :data="filterQW" :show-header="false" style="width: 100%">
            <el-table-column prop="name" :show-overflow-tooltip="true">
              <template #default="scope">
                <span class="message-title">名称: {{ scope.row.name }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="qw_token" width="200" :show-overflow-tooltip="true">
              <template #default="scope">
                <span class="message-title">token: {{ maskSensitiveData(scope.row.qw_token) }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="desc" width="200" :show-overflow-tooltip="true"></el-table-column>
            <el-table-column prop="create_time" width="180"></el-table-column>
            <el-table-column width="100">
              <template #default="scope">
                <el-button type="danger" @click="handleDel(scope.$index, scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts" name="alarm_setting">
import {reactive, ref, computed, onMounted, Ref} from 'vue';
import {ElMessage, ElMessageBox} from 'element-plus';
import type {FormInstance, FormRules} from 'element-plus';
import {getAlarmers, addAlarmers, delAlarmers} from "~/api/alarms";
import {ElForm, ElFormItem} from 'element-plus';

interface TableItem {
  id: number;
  aid: string,
  name: string,
  email: string,
  qw_token: string,
  resource: string,
  desc: string,
  extra: string;
  create_time: string;
}

const tableData = ref<TableItem[]>([]);
const alarmers = ref('first');
const rulesEmail: FormRules = {
  name: [{required: true, message: '请输入告警器名称', trigger: 'blur'}],
  email: [{required: true, message: '请输入邮件推送地址', trigger: 'blur'}],
};
const rulesQW: FormRules = {
  name: [{required: true, message: '请输入告警器名称', trigger: 'blur'}],
  qw_token: [{required: true, message: '请输入企业微信的机器人调用密钥', trigger: 'blur'}],
};
const formEmail = reactive({
  name: '',
  email: '',
  resource: '电子邮件',
  desc: '',
});
const formQW = reactive({
  name: '',
  qw_token: '',
  resource: '企微bot',
  desc: '',
});

const formRefEmail = ref<FormInstance>();
const formRefQW = ref<FormInstance>();

// 电子邮件表单提交
const submitEmailForm = () => {
  submitForm(formRefEmail, formEmail, rulesEmail);
};

// 企微机器人表单提交
const submitQWForm = () => {
  submitForm(formRefQW, formQW, rulesQW);
};

// 表单提交共用逻辑
const submitForm = (formRef: Ref<FormInstance | undefined>, formData: any, rules: FormRules) => {
  console.log("formRef!!", formRef)
  if (!formRef.value) return;
  formRef.value.validate((valid) => {
    if (valid) {
      // 提交表单
      addForm(formData);
      ElMessage.success('提交成功！');
      handleFlush();
    } else {
      return false;
    }
  });
};

// 重置电子邮件表单
const resetEmailForm = () => {
  resetForm(formRefEmail);
};

// 重置企微机器人表单
const resetQWForm = () => {
  resetForm(formRefQW);
};

// 表单重置共用逻辑
const resetForm = (formRef: Ref<FormInstance | undefined>) => {
  if (formRef.value) {
    formRef.value.resetFields();
  }
};

// 添加表单数据
const addForm = (formData: any) => {
  // 发送添加请求
  const payload = {
    name: formData.name,
    email: formData.email,
    qw_token: formData.qw_token,
    resource: formData.resource,
    desc: formData.desc,
  };
  addAlarmers(payload)
      .then(() => {
        // 添加成功后处理
        // 可以刷新数据或进行其他操作
      })
      .catch((error) => {
        console.error('添加失败：', error);
      });
};

// 数据打码
const maskSensitiveData = (data: string) => {
  const visibleLength = 3; // 可见字符的长度
  const totalLength = visibleLength + 5; // 可见字符的长度
  if (data.length <= visibleLength) {
    return data;
  } else {
    const visiblePart = data.slice(0, visibleLength);
    const maskedPart = '*'.repeat(totalLength - visiblePart.length);
    return `${visiblePart}${maskedPart}`;
  }
};

// 刷新数据
const filterEmail = ref<TableItem[]>([]);
const filterQW = ref<TableItem[]>([]);

const handleFlush = async () => {
  // 获取数据
  const res = await getAlarmers();
  tableData.value = res.data.list;

  // 过滤出 resource 为 "电子邮件" 的行数据
  filterEmail.value = tableData.value.filter(item => item.resource === '电子邮件');

  // 过滤出 resource 为 "企微机器人" 的行数据
  filterQW.value = tableData.value.filter(item => item.resource === '企微bot');
};

onMounted(() => {
  // 页面加载时刷新数据
  handleFlush();
});

// 删除操作
const handleDel = async (index: number, row: TableItem) => {
  const confirmResult = await ElMessageBox.confirm('确定要删除该告警器吗？', '警告', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  });

  if (confirmResult === 'confirm') {
    try {
      await delAlarmers({aid: row.aid}); // 调用删除请求函数
      ElMessage.success('删除成功！');
      // 从表格中移除被删除的数据
      filterEmail.value.splice(index, 1);
      filterQW.value.splice(index, 1);
    } catch (error) {
      console.error('删除失败：', error);
      ElMessage.error('删除失败！');
    }
  }
};

// const handleRestore = (index: number) => {
//   const item = state.recycle.splice(index, 1);
//   // state.read = item.concat(state.read);
// };
</script>

<style>
.message-title {
  /*cursor: pointer;*/
}

.handle-row {
  margin-top: 30px;
}
</style>
