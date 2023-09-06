<template>
  <div class="login-wrap">
    <div class="ms-login">
      <div class="ms-title">数据矿工管理系统</div>
      <el-form
        :model="param"
        :rules="rules"
        ref="login"
        label-width="0px"
        class="ms-content"
      >
        <el-form-item prop="username">
          <el-input v-model="param.username" placeholder="username">
            <template #prepend>
              <el-button :icon="User"></el-button>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input
            type="password"
            placeholder="password"
            v-model="param.password"
            @keyup.enter="submitForm(login)"
          >
            <template #prepend>
              <el-button :icon="Lock"></el-button>
            </template>
          </el-input>
        </el-form-item>
        <div class="login-btn">
          <el-button type="primary" @click="submitForm(login)">登录</el-button>
        </div>
        <p class="login-tips">Tips : 账户创建联系管理员</p>
      </el-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { login as loginProc } from "@/api/account";
import { Lock, User } from "@element-plus/icons-vue";
import type { FormInstance, FormRules } from "element-plus";
import { ElMessage } from "element-plus";
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { useAccountStore } from "~/store/account";
import { usePermissStore } from "~/store/permiss";
import { useTagsStore } from "~/store/tags";

interface LoginInfo {
  username: string;
  password: string;
}
const router = useRouter();
const accountStore = useAccountStore();

const param = reactive<LoginInfo>({
  username: "",
  password: "",
});

const rules: FormRules = {
  username: [
    {
      required: true,
      message: "请输入用户名",
      trigger: "blur",
    },
  ],
  password: [{ required: true, message: "请输入密码", trigger: "blur" }],
};
const permiss = usePermissStore();
const login = ref<FormInstance>();

const handleLogin = async () => {
  const resp = await loginProc(param);
  if (resp.isSuccess) {
    // 获取 data 里的 access_token
    const { access_token } = resp.data!;

    // element 弹出成功信息
    ElMessage.success("登录成功");
    // 本地存储数据
    localStorage.setItem("ms_username", param.username);
    // 保存 token => accountStore => useAccountStore(account.ts) =>
    accountStore.setAuthToken(access_token!);
    // 获取权限编号(todo 目前写死)
    // const keys = permiss.defaultList["normal"];
    const keys = permiss.defaultList[param.username == 'admin' ? 'admin' : 'normal'];
    // 将权限编号设置到浏览器缓存
    permiss.handleSet(keys);
    router.push("/");
  } else {
    // element 弹出错误信息
    ElMessage.error(resp.errMsg);
  }
};

const submitForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  formEl.validate((valid: boolean) => {
    if (valid) {
      handleLogin();
    } else {
      ElMessage.error("参数错误");
      return false;
    }
  });
};

const tags = useTagsStore();
tags.clearTags();
</script>

<style scoped>
.login-wrap {
  position: relative;
  width: 100%;
  height: 100%;
  background-image: url(../../assets/img/login-bg.jpg);
  background-size: 100%;
}
.ms-title {
  width: 100%;
  line-height: 50px;
  text-align: center;
  font-size: 20px;
  color: #fff;
  border-bottom: 1px solid #ddd;
}
.ms-login {
  position: absolute;
  left: 50%;
  top: 50%;
  width: 350px;
  margin: -190px 0 0 -175px;
  border-radius: 5px;
  background: rgba(255, 255, 255, 0.3);
  overflow: hidden;
}
.ms-content {
  padding: 30px 30px;
}
.login-btn {
  text-align: center;
}
.login-btn button {
  width: 100%;
  height: 36px;
  margin-bottom: 10px;
}
.login-tips {
  font-size: 12px;
  line-height: 30px;
  color: #fff;
}
</style>
