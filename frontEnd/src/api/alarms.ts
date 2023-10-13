import { API } from "~/constants/api";
import {CONTENT_TYPE, REQUEST_HEADER, REQUEST_METHOD} from "~/constants/request";
import useHttp from "~/utils/request";
import { alarmers,alarm_jobs } from "~/api/types/alarms";
import {job, project, worker} from "~/api/types/projects";
const { handleGet,handleDelete, http, handlePost } = useHttp();

// 获取告警器列表
export const getAlarmers = () => {
    return handleGet({
        url: API.ALARMS.GETALARMERS,
        method: REQUEST_METHOD.GET,
        headers: {},
    });
};

// 新增告警器
export const addAlarmers = (payload:alarmers) => {
    return handlePost({
        url: API.ALARMS.ADDALARMERS,
        headers: {
            [REQUEST_HEADER.CONTENT_TYPE]: CONTENT_TYPE.FORM_URLENCODED,
        },
        data: payload,
    });
};

// 删除告警器
export const delAlarmers = (DelData:alarmers) => {
    return handleDelete({
        url: API.ALARMS.DELALARMERS,
        method: REQUEST_METHOD.DELETE,
        headers: {},
        params: DelData,
    });
};

// 获取监控任务列表接口
export const getAlarmerJobs = () => {
    return handleGet({
        url: API.ALARMS.GETALARMERJOBS,
        method: REQUEST_METHOD.GET,
        headers: {},
    });
};

// 创建项目
export const addAlarmerJobs = (payload: alarm_jobs) => {
    return handlePost({
        url: API.ALARMS.ADDALARMERJOBS,
        headers: {
            [REQUEST_HEADER.CONTENT_TYPE]: CONTENT_TYPE.FORM_URLENCODED,
        },
        data: payload,
    });
};

// 修改项目
export const updateAlarmerJobs = (payload: alarm_jobs) => {
    return handlePost({
        url: API.ALARMS.UPDATEALARMERJOBS,
        headers: {
            [REQUEST_HEADER.CONTENT_TYPE]: CONTENT_TYPE.FORM_URLENCODED,
        },
        data: payload,
    });
};

// 删除项目
export const delAlarmerJobs = (DelData: alarm_jobs) => {
    return handleDelete({
        url: API.ALARMS.DELALARMERJOBS,
        method: REQUEST_METHOD.DELETE,
        headers: {},
        params: DelData,
    });
};

// 获取级联选择器
export const getProSub = () => {
    return handleGet({
        url: API.ALARMS.GETPROSUB,
        method: REQUEST_METHOD.GET,
        headers: {},
    });
};
