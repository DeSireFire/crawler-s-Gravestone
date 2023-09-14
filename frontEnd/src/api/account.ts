import { LoginParam, LoginResponse, UsersResponse } from "~/api/types/account";
import { API } from "~/constants/api";
import {CONTENT_TYPE, REQUEST_HEADER, REQUEST_METHOD} from "~/constants/request";
import useHttp from "~/utils/request";

const { handlePost,handleGet } = useHttp();

// 登录用户
export const login = (payload: LoginParam) => {
  return handlePost<LoginResponse>({
    url: API.ACCOUNT.LOGIN,
    headers: {
      [REQUEST_HEADER.CONTENT_TYPE]: CONTENT_TYPE.FORM_URLENCODED,
    },
    data: payload,
  });
};

// 新增用户
export const add_user = (payload: UsersResponse) => {
  return handlePost({
    url: API.ACCOUNT.ADDUSER,
    headers: {
      [REQUEST_HEADER.CONTENT_TYPE]: CONTENT_TYPE.FORM_URLENCODED,
    },
    data: payload,
  });
};

// 编辑用户
export const edit_user = (payload: UsersResponse) => {
  return handlePost({
    url: API.ACCOUNT.EDITUSER,
    headers: {
      [REQUEST_HEADER.CONTENT_TYPE]: CONTENT_TYPE.FORM_URLENCODED,
    },
    data: payload,
  });
};

// 获取用户列表
export const get_users = () => {
  return handleGet({
    url: API.ACCOUNT.GETUSERS,
    method: REQUEST_METHOD.GET,
    headers: {},
  });
};

// 删除用户
export const del_user = (payload: UsersResponse) => {
  return handlePost({
    url: API.ACCOUNT.DELUSER,
    headers: {
      [REQUEST_HEADER.CONTENT_TYPE]: CONTENT_TYPE.FORM_URLENCODED,
    },
    data: payload,
  });
};
