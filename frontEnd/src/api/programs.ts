import {API, PROGRAMS} from "~/constants/api";
import {CONTENT_TYPE, REQUEST_HEADER, REQUEST_METHOD} from "~/constants/request";
import useHttp from "~/utils/request";
import { program } from "~/api/types/programs";
import {job, project, worker} from "~/api/types/projects";
import {alarmers} from "~/api/types/alarms";
const { handleGet,handleDelete, http, handlePost } = useHttp();

// 获取列表
export const getPrograms = () => {
    return handleGet({
        url: API.PROGRAMS.GETPROGRAMS,
        method: REQUEST_METHOD.GET,
        headers: {},
    });
};

// 新增程序
export const addPrograms = (payload:program) => {
    return handlePost({
        url: API.PROGRAMS.ADDPROGRAM,
        headers: {
            [REQUEST_HEADER.CONTENT_TYPE]: CONTENT_TYPE.FORM_URLENCODED,
        },
        data: payload,
    });
};

// 删除程序
export const delPrograms = (DelData:program) => {
    return handleDelete({
        url: API.PROGRAMS.DELPROGRAM,
        method: REQUEST_METHOD.DELETE,
        headers: {},
        params: DelData,
    });
};

// 获取程序信息
export const getProgram = (ProgramInfo:any) => {
    return handleGet({
        url: API.PROGRAMS.GETPROGRAM,
        method: REQUEST_METHOD.GET,
        headers: {},
        params: ProgramInfo,
    });
};
