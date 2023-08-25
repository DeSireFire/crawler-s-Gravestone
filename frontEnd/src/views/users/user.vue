<template>
	<div>
		<el-row :gutter="20">
			<el-col :span="24">
				<el-card shadow="hover">
					<template #header>
						<div class="clearfix">
							<span>基础信息</span>
						</div>
					</template>
					<div class="info">
						<div class="info-image" @click="showDialog">
							<el-avatar :size="100" :src="avatarImg" />
							<span class="info-edit">
								<i class="el-icon-lx-camerafill"></i>
							</span>
						</div>
						<div class="info-name">{{ name }}</div>
						<div class="info-desc">{{form.desc}}</div>
					</div>
				</el-card>
			</el-col>
		</el-row>
    <br/>
    <el-row :gutter="20">
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header>
            <div class="clearfix">
              <span>账户编辑</span>
            </div>
          </template>
          <el-form label-width="90px">
            <el-form-item label="用户名："> {{ name }} </el-form-item>
            <el-form-item label="旧密码：">
              <el-input type="password" v-model="form.old"></el-input>
            </el-form-item>
            <el-form-item label="新密码：">
              <el-input type="password" v-model="form.new"></el-input>
            </el-form-item>
            <el-form-item label="个人简介：">
              <el-input v-model="form.desc"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="onSubmit">保存</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header>
            <div class="clearfix">
              <span>系统设置</span>
            </div>
          </template>
          <el-form label-width="100px">
            <el-form-item label="开启标签页：">
              <el-switch
                  v-model="tagsSwitch"
              />
            </el-form-item>
            <el-form-item>
<!--              <el-button type="primary" @click="handleSystemChange">保存</el-button>-->
<!--              <el-button type="primary">保存</el-button>-->
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
    </el-row>
		<el-dialog title="裁剪图片" v-model="dialogVisible" width="600px">
			<vue-cropper
				ref="cropper"
				:src="imgSrc"
				:ready="cropImage"
				:zoom="cropImage"
				:cropmove="cropImage"
				style="width: 100%; height: 400px"
			></vue-cropper>

			<template #footer>
				<span class="dialog-footer">
					<el-button class="crop-demo-btn" type="primary"
						>选择图片
						<input class="crop-input" type="file" name="image" accept="image/*" @change="setImage" />
					</el-button>
					<el-button type="primary" @click="saveAvatar">上传并保存</el-button>
				</span>
			</template>
		</el-dialog>
	</div>
</template>

<script setup lang="ts" name="user">
import { reactive, ref, onMounted, watch } from 'vue';
import { useTagsStore } from '~/store/tags';
import { get_system_settings } from '~/store/tags';
import VueCropper from 'vue-cropperjs';
import 'cropperjs/dist/cropper.css';
import {ElMessage} from "element-plus";
const avatar = 'https://avatars.githubusercontent.com/u/64947085?v=4'

// 从 localStorage 中获取 system_settings 数据，如果不存在则创建一个默认值
const systemSettingsJSON = localStorage.getItem('system_settings') as string;
const defaultSystemSettings = { tags_switch: false }; // 默认值可以根据实际需求调整
const systemSettings = ref(JSON.parse(systemSettingsJSON) || defaultSystemSettings);

// 提取 tags_switch 布尔值，并通过双向绑定的方式与 el-switch 控件关联
const tagsSwitch = ref(systemSettings.value.tags_switch);

// 监听 tagsSwitch 的变化，当值发生变化时更新 localStorage 中的数据
onMounted(() => {
  // 监听 tagsSwitch 的变化，并将其同步到 localStorage 中的 system_settings 对象
  watch(tagsSwitch, (newValue) => {
    systemSettings.value.tags_switch = newValue;
    localStorage.setItem('system_settings', JSON.stringify(systemSettings.value));
    if (!systemSettings.value.tags_switch) {
      closeAll();
    };
  });
});

// 关闭全部标签
const tags = useTagsStore();
const closeAll = () => {
  tags.clearTags();
};


const name = localStorage.getItem('ms_username');
const form = reactive({
	old: '',
	new: '',
  delivery: '',
	desc: '不可能！我的代码怎么可能会有bug！'
});
const onSubmit = () => {};

const avatarImg = ref(avatar);
const imgSrc = ref('');
const cropImg = ref('');
const dialogVisible = ref(false);
const cropper: any = ref();

const showDialog = () => {
	dialogVisible.value = true;
	imgSrc.value = avatarImg.value;
};

const setImage = (e: any) => {
	const file = e.target.files[0];
	if (!file.type.includes('image/')) {
		return;
	}
	const reader = new FileReader();
	reader.onload = (event: any) => {
		dialogVisible.value = true;
		imgSrc.value = event.target.result;
		cropper.value && cropper.value.replace(event.target.result);
	};
	reader.readAsDataURL(file);
};

const cropImage = () => {
	cropImg.value = cropper.value.getCroppedCanvas().toDataURL();
};

const saveAvatar = () => {
	avatarImg.value = cropImg.value;
	dialogVisible.value = false;
};
</script>

<style scoped>
.info {
	text-align: center;
	padding: 35px 0;
}
.info-image {
	position: relative;
	margin: auto;
	width: 100px;
	height: 100px;
	background: #f8f8f8;
	border: 1px solid #eee;
	border-radius: 50px;
	overflow: hidden;
}

.info-edit {
	display: flex;
	justify-content: center;
	align-items: center;
	position: absolute;
	left: 0;
	top: 0;
	width: 100%;
	height: 100%;
	background: rgba(0, 0, 0, 0.5);
	opacity: 0;
	transition: opacity 0.3s ease;
}
.info-edit i {
	color: #eee;
	font-size: 25px;
}
.info-image:hover .info-edit {
	opacity: 1;
}
.info-name {
	margin: 15px 0 10px;
	font-size: 24px;
	font-weight: 500;
	color: #262626;
}
.crop-demo-btn {
	position: relative;
}
.crop-input {
	position: absolute;
	width: 100px;
	height: 40px;
	left: 0;
	top: 0;
	opacity: 0;
	cursor: pointer;
}
</style>
