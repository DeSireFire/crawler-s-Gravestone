import { API } from "~/constants/api";
import {CONTENT_TYPE, REQUEST_HEADER, REQUEST_METHOD} from "~/constants/request";
import useHttp from "~/utils/request";
import { alarmers,alarm_jobs } from "~/api/types/alarms";
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
