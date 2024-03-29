import { API } from "~/constants/api";
import {CONTENT_TYPE, REQUEST_HEADER, REQUEST_METHOD} from "~/constants/request";
import useHttp from "~/utils/request";
import { project,worker,job } from "~/api/types/projects";
const { handleGet,handleDelete, http, handlePost } = useHttp();

// 获取项目列表
export const getProjects = () => {
    return handleGet({
        url: API.PROJECTS.GETPROJECTS,
        method: REQUEST_METHOD.GET,
        headers: {},
    });
};

// 获取项目列表
export const getProjectsNames = () => {
    return handleGet({
        url: API.PROJECTS.GETPROJECTSNAMES,
        method: REQUEST_METHOD.GET,
        headers: {},
    });
};

// 获取指定项目信息
export const getProject = (params:any) => {
    return handleGet({
        url: API.PROJECTS.GETPROJECT,
        method: REQUEST_METHOD.GET,
        headers: {},
        params,
    });
};

// 创建项目
export const addProjects = (payload: project) => {
    return handlePost({
        url: API.PROJECTS.ADDPROJECT,
        headers: {
            [REQUEST_HEADER.CONTENT_TYPE]: CONTENT_TYPE.FORM_URLENCODED,
        },
        data: payload,
    });
};

// 修改项目
export const updateProjects = (payload: project) => {
    return handlePost({
        url: API.PROJECTS.UPDATEPROJECT,
        headers: {
            [REQUEST_HEADER.CONTENT_TYPE]: CONTENT_TYPE.FORM_URLENCODED,
        },
        data: payload,
    });
};

// 删除项目
export const delProjects = (DelData:project) => {
    return handleDelete({
        url: API.PROJECTS.DELPROJECT,
        method: REQUEST_METHOD.DELETE,
        headers: {},
        params: DelData,
    });
};

// 获取工作流列表
export const getWorkers = (params: any) => {
    return handleGet({
        url: API.PROJECTS.GETWORKERS,
        method: REQUEST_METHOD.GET,
        headers: {},
        params,
    });
};

// 获取工作流列表
// wid:xxx
export const getWorker = (params: any) => {
    return handleGet({
        url: API.PROJECTS.GETWORKER,
        method: REQUEST_METHOD.GET,
        headers: {},
        params,
    });
};

// 新增工作流
export const addWorkers = (payload:worker) => {
    return handlePost({
        url: API.PROJECTS.ADDWORKERS,
        headers: {
            [REQUEST_HEADER.CONTENT_TYPE]: CONTENT_TYPE.FORM_URLENCODED,
        },
        data: payload,
    });
};

// 删除工作流
export const delWorkers = (DelData:worker) => {
    return handleDelete({
        url: API.PROJECTS.DELWORKERS,
        method: REQUEST_METHOD.DELETE,
        headers: {},
        params: DelData,
    });
};

// 修改工作流
export const updateWorkers = (payload: worker) => {
    return handlePost({
        url: API.PROJECTS.UPDATEWORKERS,
        headers: {
            [REQUEST_HEADER.CONTENT_TYPE]: CONTENT_TYPE.FORM_URLENCODED,
        },
        data: payload,
    });
};

// 获取任务实例列表(带参数)
export const getJobs = (params: any) => {
    return handleGet({
        url: API.PROJECTS.GETJOBS,
        method: REQUEST_METHOD.GET,
        headers: {},
        params,
    });
};

// 获取任务实例列表(带参数)
export const updateStatusFinished = (params: any) => {
    return handleGet({
        url: API.PROJECTS.UPDATESTATUSFINISHED,
        method: REQUEST_METHOD.GET,
        headers: {},
        params,
    });
};

// 删除工作流
export const delJobs = (DelData:job) => {
    return handleDelete({
        url: API.PROJECTS.DELJOBS,
        method: REQUEST_METHOD.DELETE,
        headers: {},
        params: DelData,
    });
};


// 获取任务日志
// {jid:xxx}
export const getLogContent = (logInfo:any) => {
    return handleGet({
        url: API.PROJECTS.GETLOG,
        method: REQUEST_METHOD.GET,
        headers: {},
        params: logInfo,
    });
};

// 下载任务日志文件
// {jid:xxx}
export const downLoadLog = (logInfo:any) => {
    return handleGet({
        url: API.PROJECTS.DOWNLOADLOG,
        method: REQUEST_METHOD.GET,
        headers: {},
        params: logInfo,
    });
};


// 获取项目首页折线图
// {pid:xxx}
export const getPTask = (pid:any) => {
    return handleGet({
        url: API.PROJECTS.GETPTASKS,
        method: REQUEST_METHOD.GET,
        headers: {},
        params: pid,
    });
};
