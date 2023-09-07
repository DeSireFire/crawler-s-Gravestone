import {reactive, ref} from "vue";
import {getLogs,delLogs} from "~/api/workerLogs";
// import {pageTotal, tableData, query, TableItem} from "~/constants/worker_logs";

interface TableItem {
    id: number;
    name: string;
    nicename: string;
    status: string;
    create: string;
    role: string;
    password: string;
    lastlogin: string;
}

const query = reactive({
    filterWord: '',
    keyword: '',
    pageIndex: 1,
    pageSize: 100
});
const tableData = ref<TableItem[]>([]);
const pageTotal = ref(0);

// 获取表格数据
const updateView = (page_num: number, datas: [] = []) => {
    if (!datas) {
        datas = JSON.parse(localStorage.getItem('workerLogs') as string).list;
    }
    // const datas = JSON.parse(localStorage.getItem('workerLogs') as string).list;
    // 传递页码
    query.pageIndex = page_num;
    // 获取每个分页得大小
    let page_size = query.pageSize
    // 计算本页需要展示得片段
    let index_start = 0
    let index_end = query.pageSize
    if (page_num == 1 /* 第1页和第0页，内容一致 */) {
        index_start = 0
    } else {
        index_start = (page_num - 1) * page_size
        index_end = (page_num - 1) * page_size + page_size
    }
    return datas.slice(index_start, index_end)
}

// 数据关键词搜索
const keywordSearch = (kw: string, datas: TableItem[] = []) => {
    // console.log("检索词", kw);
    // console.log("datas", datas);
    return datas.filter((item) => {
        return item.name.includes(kw) || item.nicename.includes(kw) || item.status.includes(kw);
    })
};


// api 输出
export const um_api = {
    updateView,
    keywordSearch,
    query,
};
