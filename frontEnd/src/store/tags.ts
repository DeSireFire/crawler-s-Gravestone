import { defineStore } from 'pinia';
import { ref, reactive } from 'vue';
interface ListItem {
	name: string;
	path: string;
	title: string;
}
interface systemItem {
	tags_switch: boolean;
}
let tags_switch:boolean = true;
let system_settings:systemItem = <systemItem>{};
export const get_system_settings = () => {
	// 查询 localStorage 是否包含名为 "system_settings" 的数据
	const containsName = localStorage.getItem('system_settings') !== null;
	if (containsName) {
		system_settings = JSON.parse(localStorage.getItem('system_settings') as string);
		tags_switch = system_settings.tags_switch as boolean;
	} else {
		const system_settings_base = reactive({
			// 浏览历史tags标签开关
			tags_switch: tags_switch,
		})
		// 缓存数据
		localStorage.setItem('system_settings', JSON.stringify(system_settings_base));
	}
}


export const useTagsStore = defineStore('tags', {
	state: () => {
		return {
			list: <ListItem[]>[]
		};
	},
	getters: {
		show: state => {
			return state.list.length > 0;
		},
		nameList: state => {
			return state.list.map(item => item.name);
		}
	},
	actions: {
		delTagsItem(index: number) {
			this.list.splice(index, 1);
		},
		setTagsItem(data: ListItem) {
			// 开关判断关闭时，不再新增标签页
			get_system_settings();
			if (tags_switch) {
				// console.log("检测开关状态：", tags_switch)
				this.list.push(data);
			}
		},
		clearTags() {
			this.list = [];
		},
		closeTagsOther(data: ListItem[]) {
			this.list = data;
		},
		closeCurrentTag(data: any) {
			for (let i = 0, len = this.list.length; i < len; i++) {
				const item = this.list[i];
				if (item.path === data.$route.fullPath) {
					if (i < len - 1) {
						data.$router.push(this.list[i + 1].path);
					} else if (i > 0) {
						data.$router.push(this.list[i - 1].path);
					} else {
						data.$router.push('/');
					}
					this.list.splice(i, 1);
					break;
				}
			}
		}
	}
});
