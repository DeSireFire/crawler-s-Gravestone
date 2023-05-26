export enum REQUEST_METHOD {
  GET = "get",
  POST = "post",
  PUT = "put",
  DELETE = "delete",
  PATCH = "patch",
}

// 常量请求头
export enum REQUEST_HEADER {
  CONTENT_TYPE = "Content-Type",
  // add more headers here
}

// post请求的content_type类型
export enum CONTENT_TYPE {
  JSON = "application/json",
  FORM_URLENCODED = "application/x-www-form-urlencoded",
  FORM_DATA = "multipart/form-data",
}
