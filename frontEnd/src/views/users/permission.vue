<template>
	<div class="container">
		<div class="plugins-tips">用户权限管理(开发中..)</div>
		<div class="mgb20">
			<span class="label">角色：</span>
			<el-select v-model="role" @change="handleChange">
				<el-option label="超级管理员" value="admin"></el-option>
				<el-option label="普通用户" value="normal"></el-option>
			</el-select>
		</div>
		<div class="mgb20 tree-wrapper">
			<el-tree
				ref="tree"
				:data="data"
				node-key="id"
				default-expand-all
				show-checkbox
				:default-checked-keys="checkedKeys"
			/>
		</div>
		<el-button type="primary" @click="onSubmit">保存权限</el-button>
	</div>
</template>

<script setup lang="ts" name="permission">
import { ref } from 'vue';
import { ElTree } from 'element-plus';
import { usePermissStore } from '~/store/permiss';

const role = ref<string>('admin');

interface Tree {
	id: string;
	label: string;
	children?: Tree[];
}

const data: Tree[] = [
	{
		id: '1',
		label: '系统首页'
	},
  {
    id: '2',
    label: '用户管理',
    children: [
      {
        id: '21',
        label: '权限管理'
      },
      {
        id: '22',
        label: '账号管理'
      },
      {
        id: '23',
        label: '个人中心'
      },
    ]
  },
  {
    id: '3',
    label: '日志管理',
    children: [
      {
        id: '31',
        label: '任务日志'
      },
    ]
  },
];

const permiss = usePermissStore();

// 获取当前权限
const checkedKeys = ref<string[]>([]);
const getPremission = () => {
	// 请求接口返回权限
	checkedKeys.value = permiss.defaultList[role.value];
  console.log("checkedKeys.value", checkedKeys.value)
};
getPremission();

// 保存权限
const tree = ref<InstanceType<typeof ElTree>>();
const onSubmit = () => {
	// 获取选中的权限
	console.log(tree.value!.getCheckedKeys(false));
};

const handleChange = (val: string[]) => {
  console.log('handleChange', val)
	tree.value!.setCheckedKeys(permiss.defaultList[role.value]);
};
</script>

<style scoped>
.tree-wrapper {
	max-width: 500px;
}
.label {
	font-size: 14px;
}
</style>
