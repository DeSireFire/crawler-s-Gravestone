import { API } from "~/constants/api";
import {CONTENT_TYPE, REQUEST_HEADER, REQUEST_METHOD} from "~/constants/request";
import useHttp from "~/utils/request";
import {dashInfo} from "~/api/types/dashboard";

const { handleGet, http } = useHttp();

export const getDashInfo = () => {
    return handleGet({
        url: API.DASHBOARD.DBOARDINFO,
        method: REQUEST_METHOD.GET,
        headers: {},
    });
};

export const getDashJobs = () => {
    return handleGet({
        url: API.DASHBOARD.DBOARDJOBS,
        method: REQUEST_METHOD.GET,
        headers: {},
    });
};

export const getDashLogs = () => {
    return handleGet({
        url: API.DASHBOARD.DBOARDLOGTOTAL,
        method: REQUEST_METHOD.GET,
        headers: {},
    });
};

// 业务统计
// 淘系调用统计
export const getDashTB = () => {
    return handleGet({
        url: API.DASHBOARD.DBOARDTAOBAO,
        method: REQUEST_METHOD.GET,
        headers: {},
    });
};
