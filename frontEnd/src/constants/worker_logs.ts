import {reactive, ref} from "vue";

export interface TableItem {
  id: number;
  log_project: string;
  name: string;
  remarks: string;
  address: string;
}

export const query = reactive({
  address: '',
  filterWord: '',
  keyword: '',
  pageIndex: 1,
  pageSize: 10,
});

export const tableData = ref<TableItem[]>([]);
export let pageTotal = ref(0);

