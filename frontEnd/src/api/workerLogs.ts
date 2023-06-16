import { API } from "~/constants/api";
import {CONTENT_TYPE, REQUEST_HEADER, REQUEST_METHOD} from "~/constants/request";
import useHttp from "~/utils/request";
import { LogInfo } from "~/api/types/workerLogs";
const { handleGet,handleDelete, http } = useHttp();
// 获取日志文件列表
export const getLogs = () => {
    return handleGet({
        url: API.WORKERLOGS.GETLOGS,
        method: REQUEST_METHOD.GET,
        headers: {},
    });
};

// 删除指定日志文件
export const delLogs = (DelData:LogInfo) => {
    return handleDelete({
        // url: `${API.WORKERLOGS.DELLOGS}/${DelData}`,
        url: API.WORKERLOGS.DELLOGS,
        method: REQUEST_METHOD.DELETE,
        headers: {},
        params: DelData,
    });
};

// 获取日志文件内容
export const getLogContent = (logInfo:LogInfo) => {
    return handleGet({
        url: API.WORKERLOGS.GETLOGCONTENT,
        method: REQUEST_METHOD.GET,
        headers: {},
        params: logInfo,
    });
};
