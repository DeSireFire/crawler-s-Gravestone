import { API } from "~/constants/api";
import {CONTENT_TYPE, REQUEST_HEADER, REQUEST_METHOD} from "~/constants/request";
import useHttp from "~/utils/request";
import { project } from "~/api/types/projects";
import {LogInfo} from "~/api/types/workerLogs";
const { handleGet,handleDelete, http, handlePost } = useHttp();

// 获取项目列表
export const getProjects = () => {
    return handleGet({
        url: API.PROJECTS.GETPROJECTS,
        method: REQUEST_METHOD.GET,
        headers: {},
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
export const getWorkers = () => {
    return handleGet({
        url: API.PROJECTS.GETWORKERS,
        method: REQUEST_METHOD.GET,
        headers: {},
    });
};
