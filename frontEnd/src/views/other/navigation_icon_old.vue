<template>
	<div class="container">
		<h2>平台导航</h2>
		<p style="line-height: 50px">
			点击相应图标即可完成页面跳转：（共{{ iconList.length }}个图标）
		</p>
		<br />
		<div class="search-box">
			<el-input class="search" size="large" v-model="keyword" clearable placeholder="需要搜索的网站关键字"></el-input>
		</div>
		<ul>
			<li class="icon-li" v-for="(item, index) in list" :key="index">
				<div class="icon-li-content">
					<i :class="`el-icon-lx-tag`"></i>
<!--					<i :class="`el-icon-lx-${item}`"></i>-->
					<span>{{ item }}</span>
				</div>
			</li>
		</ul>
	</div>
</template>

<script setup lang="ts" name="icon">
import { computed, ref } from 'vue';

const iconList: Array<string> = [
	'tag',
	'tag',
	'tag',
];
const keyword = ref('');
const list = computed(() => {
	return iconList.filter(item => {
		return item.indexOf(keyword.value) !== -1;
	});
});
</script>

<style scoped>
.search-box {
	text-align: center;
	margin-top: 10px;
}
.search {
	width: 300px;
}
ul,
li {
	list-style: none;
}
.icon-li {
	display: inline-block;
	padding: 10px;
	width: 120px;
	height: 120px;
}
.icon-li-content {
	display: flex;
	height: 100%;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	cursor: pointer;
}
.icon-li-content i {
	font-size: 36px;
	color: #606266;
}
.icon-li-content span {
	margin-top: 10px;
	color: #787878;
}
</style>
