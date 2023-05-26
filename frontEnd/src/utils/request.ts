import axios, {AxiosInstance, AxiosRequestConfig, AxiosResponse} from "axios";
import { RestResponse } from "~/api/types/base";
import { BASE_URL } from "~/constants/api";
import { REQUEST_METHOD } from "~/constants/request";

axios.defaults.headers.common['Access-Control-Allow-Origin'] = '*';

const http: AxiosInstance = axios.create({
  baseURL: BASE_URL,
  timeout: 5000,
});

http.interceptors.request.use(
  function (config) {
    return config;
  },
  function (error) {
    return Promise.reject(error);
  }
);

http.interceptors.response.use(
  function (response) {
    return response;
  },
  function (error) {
    return Promise.reject(error);
  }
);

// async function request<T>(args: AxiosRequestConfig) {
//   try {
//     const response = await http.request(args);
//     const { data, err_msg, err_code } = response.data;
//     return RestResponse.from<T>({
//       httpCode: response.status,
//       httpStatus: response.statusText,
//       data: data,
//       errMsg: err_msg,
//       errCode: err_code,
//     });
//   } catch (error) {
//     if (axios.isAxiosError(error)) {
//       const response = error.response;
//       return RestResponse.from<T>({
//         httpCode: response?.status || 500,
//         httpStatus: response?.statusText || "Internal Server Error",
//         errMsg: response?.data?.err_msg || error.message,
//         errCode: response?.data?.err_code || "500",
//       });
//     } else {
//       return RestResponse.from<T>({
//         httpCode: 500,
//         httpStatus: "Internal Server Error",
//         errMsg: (error as Error).message,
//         errCode: "500",
//       });
//     }
//   }
// }

async function request<T>(args: AxiosRequestConfig, semanticData = true) {
  try {
    const response = await http.request(args);
    const { data, err_msg, err_code } = response.data;
    // if (!semanticData) {
    //   return response as unknown as AxiosResponse<T>;
    // }
    return RestResponse.from<T>({
      httpCode: response.status,
      httpStatus: response.statusText,
      data: data,
      errMsg: err_msg,
      errCode: err_code,
    });
  } catch (error) {
    // if (!semanticData) {
    //   throw error;
    // }
    if (axios.isAxiosError(error)) {
      const response = error.response;
      return RestResponse.from<T>({
        httpCode: response?.status || 500,
        httpStatus: response?.statusText || "Internal Server Error",
        errMsg: response?.data?.err_msg || error.message,
        errCode: response?.data?.err_code || "500",
      });
    } else {
      return RestResponse.from<T>({
        httpCode: 500,
        httpStatus: "Internal Server Error",
        errMsg: (error as Error).message,
        errCode: "500",
      });
    }
  }
}

// async function raw_request<T>(args: AxiosRequestConfig) {
//   try {
//     const response = await http.request(args);
//     const { data, err_msg, err_code } = response.data;
//     return response as unknown as AxiosResponse<T>;
//   } catch (error) {
//     // throw error;
//     if (axios.isAxiosError(error)) {
//       const response = error.response;
//       return RestResponse.from<T>({
//         httpCode: response?.status || 500,
//         httpStatus: response?.statusText || "Internal Server Error",
//         errMsg: response?.data?.err_msg || error.message,
//         errCode: response?.data?.err_code || "500",
//       });
//     } else {
//       return RestResponse.from<T>({
//         httpCode: 500,
//         httpStatus: "Internal Server Error",
//         errMsg: (error as Error).message,
//         errCode: "500",
//       });
//     }
//   }
// }

const useHttp = () => ({
  http,

  request,

  handleGet<T>(args: AxiosRequestConfig) {
    return request<T>({
      method: REQUEST_METHOD.GET,
      ...args,
    });
  },

  handlePost<T>(args: AxiosRequestConfig) {
    return request<T>({
      method: REQUEST_METHOD.POST,
      ...args,
    });
  },

  handlePatch<T>(args: AxiosRequestConfig) {
    return request<T>({
      method: REQUEST_METHOD.PATCH,
      ...args,
    });
  },

  handlePut<T>(args: AxiosRequestConfig) {
    return request<T>({
      method: REQUEST_METHOD.PUT,
      ...args,
    });
  },

  handleDelete<T>(args: AxiosRequestConfig) {
    return request<T>({
      method: REQUEST_METHOD.DELETE,
      ...args,
    });
  },
});

export default useHttp;
