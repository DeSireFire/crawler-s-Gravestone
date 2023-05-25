export enum REQUEST_METHOD {
  GET = "get",
  POST = "post",
  PUT = "put",
  DELETE = "delete",
  PATCH = "patch",
}

export enum REQUEST_HEADER {
  CONTENT_TYPE = "Content-Type",
  // add more headers here
}

export enum CONTENT_TYPE {
  JSON = "application/json",
  FORM_URLENCODED = "application/x-www-form-urlencoded",
  FORM_DATA = "multipart/form-data",
}
