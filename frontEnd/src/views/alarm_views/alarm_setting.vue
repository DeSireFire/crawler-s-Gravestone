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
                <el-form ref="formRef" :rules="rulesEmail" :model="formEmail" label-width="100px">
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
                    <el-button type="primary" @click="onSubmitE(formRef)">表单提交</el-button>
                    <el-button @click="onReset(formRef)">重置表单</el-button>
                  </el-form-item>
                </el-form>
              </div>
            </el-tab-pane>
            <el-tab-pane :label="`企微机器人设置`" name="second">
              <div class="form-box">
                <el-form ref="formRef" :rules="rulesQW" :model="formQW" label-width="100px">
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
                    <el-button type="primary" @click="onSubmitQ(formRef)">表单提交</el-button>
                    <el-button @click="onReset(formRef)">重置表单</el-button>
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
          <el-table :data="state.unread" :show-header="false" style="width: 100%">
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
                <!--                <el-button type="danger" @click="handleDel(scope.$index)">删除</el-button>-->
                <el-button type="danger">删除</el-button>
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
            <b>企信机器人告警器</b>:
          </div>
          <el-table :data="state.read" :show-header="false" style="width: 100%">
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
                <!--                <el-button type="danger" @click="handleDel(scope.$index)">删除</el-button>-->
                <el-button type="danger">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts" name="alarm_setting">
import {reactive, ref} from 'vue';
import {ElMessage} from 'element-plus';
import type {FormInstance, FormRules} from 'element-plus';

const state = reactive({
  unread: [
    {
      create_time: '2018-04-19 20:00:00',
      name: '国家药典委员会告警',
      email: 'xx@qq.com',
      desc: '主数据采集药典委员会任务推送',
    },
    {
      create_time: '2018-04-19 21:00:00',
      name: '企查查企业信息采集',
      email: 'xx@qq.com',
      desc: '主数据采集药典委员会任务推送',
    }
  ],
  read: [
    {
      create_time: '2018-04-19 20:00:00',
      name: '国家药典委员会告警',
      qw_token: '325g455',
      desc: '主数据数据研究群',
    },
  ],
  recycle: [
    {
      date: '2018-04-19 20:00:00',
      title: '【系统通知】该系统将于今晚凌晨2点到5点进行升级维护'
    }
  ]
});

interface TableItem {
  id: number;
  name: string,
  email: string,
  qw_token: string,
  resource: string,
  desc: string,
  create_time: string;
  update_time: string;
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
const formRef = ref<FormInstance>();
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

// 提交
const onSubmitE = (formEl: FormInstance | undefined) => {
  // 表单校验
  if (!formEl) return;
  formEl.validate((valid) => {
    if (valid) {
      console.log(formEmail);
      ElMessage.success('提交成功！');
    } else {
      return false;
    }
  });
};
const onSubmitQ = (formEl: FormInstance | undefined) => {
  // 表单校验
  if (!formEl) return;
  formEl.validate((valid) => {
    if (valid) {
      console.log(formQW);
      ElMessage.success('提交成功！');
    } else {
      return false;
    }
  });
};
// 重置
const onReset = (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  formEl.resetFields();
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

const handleRead = (index: number) => {
  const item = state.unread.splice(index, 1);
  // state.read = item.concat(state.read);
};
const handleDel = (index: number) => {
  const item = state.read.splice(index, 1);
  // state.recycle = item.concat(state.recycle);
};
const handleRestore = (index: number) => {
  const item = state.recycle.splice(index, 1);
  // state.read = item.concat(state.read);
};
</script>

<style>
.message-title {
  /*cursor: pointer;*/
}

.handle-row {
  margin-top: 30px;
}
</style>
