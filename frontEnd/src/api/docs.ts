import { API } from "~/constants/api";
import {CONTENT_TYPE, REQUEST_HEADER, REQUEST_METHOD} from "~/constants/request";
import useHttp from "~/utils/request";
import {alarm_jobs} from "~/api/types/alarms";
const { handleGet,handleDelete, http, handlePost } = useHttp();

// 创建文章
export const updateDoc = (payload: any) => {
    return handlePost({
        url: API.DOCS.UPDATEDOC,
        headers: {
            [REQUEST_HEADER.CONTENT_TYPE]: CONTENT_TYPE.FORM_URLENCODED,
        },
        data: payload,
    });
};

// 获取共享文档
// export const getShape = (params: any) => {
export const getShape = () => {
    return handleGet({
        url: API.DOCS.GETSHAPE,
        method: REQUEST_METHOD.GET,
        headers: {},
        // params,
    });
};

// 获取个人文档
export const getMydocs = (params: any) => {
    return handleGet({
        url: API.DOCS.GETMYDOCS,
        method: REQUEST_METHOD.GET,
        headers: {},
        params,
    });
};

// 阅读指定文档
export const getDoc = (params: any) => {
    return handleGet({
        url: API.DOCS.GETDOC,
        method: REQUEST_METHOD.GET,
        headers: {},
        params,
    });
};

// 删除指定文档
export const delDoc = (params: any) => {
    return handleDelete({
        url: API.DOCS.DELMYDOCS,
        method: REQUEST_METHOD.DELETE,
        headers: {},
        params: params,
    });
};
