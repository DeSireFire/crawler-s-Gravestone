import {reactive, ref} from "vue";
import {getLogs,delLogs} from "~/api/workerLogs";
import {pageTotal, tableData, query, TableItem} from "~/constants/worker_logs";
import {ACCOUNT, EXTRALS, WORKERLOGS} from "~/constants/api";
// import { DelLogData } from "~/api/types/workerLogs";

// 获取表格数据
const getData = () => {
    getLogs().then(res => {
        // console.log("res.data", res.data)
        tableData.value = res.data.list.slice(0, query.pageSize);
        pageTotal.value = res.data.pageTotal || 1;
        localStorage.setItem('workerLogs', JSON.stringify(res.data));
    });
};

//翻页表格数据
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
        return item.name.includes(kw) || item.remarks.includes(kw) || item.address.includes(kw);
    })
};

// 所属项目筛选
const logProjectFilter = (filterWord: string, datas: TableItem[] = []) => {
    // console.log("项目筛选", filterWord);
    // console.log("datas", datas);
    return datas.filter((item) => {
        return item.log_project.includes(filterWord);
    })
};

// 删除日志文件
const deleteLogfile = async (delLogData: any) => {
    // 获取数据
    const response = (await delLogs(delLogData));
    let msg = response.errMsg ?? "无"
    console.log("delLogData-res",msg)
    return response.data
};

// api 输出
export const wl_api = {
    getData,
    updateView,
    keywordSearch,
    logProjectFilter,
    deleteLogfile,
};
