import { LoginParam, LoginResponse } from "~/api/types/account";
import { API } from "~/constants/api";
import { CONTENT_TYPE, REQUEST_HEADER } from "~/constants/request";
import useHttp from "~/utils/request";

const { handlePost } = useHttp();

export const login = (payload: LoginParam) => {
  return handlePost<LoginResponse>({
    url: API.ACCOUNT.LOGIN,
    headers: {
      [REQUEST_HEADER.CONTENT_TYPE]: CONTENT_TYPE.FORM_URLENCODED,
    },
    data: payload,
  });
};
