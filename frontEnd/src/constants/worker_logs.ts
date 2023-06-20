import {reactive, ref} from "vue";

export interface TableItem {
  id: string;
  log_project: string;
  log_projects: Array<string>;
  name: string;
  remarks: string;
  address: string;
  create_time: number;
  modify_time: number;
}

export interface textAreaItem {
  minRows: number;
  maxRows: number;
}

export const query = reactive({
  address: '',
  filterWord: '',
  keyword: '',
  pageIndex: 1,
  pageSize: 10,
  log_projects: [],
});

export const tableData = ref<TableItem[]>([]);
export let pageTotal = ref(0);

// 表格编辑时弹窗和保存
export const editVisible = ref(false);
export let form = reactive({
  name: '',
  address: ''
});

// 表格查看日志内容
