export class RestResponse<T extends any> {
  httpCode?: number;
  httpStatus?: string;
  data?: any;
  errCode?: string;
  errMsg?: string;

  constructor(data?: Partial<RestResponse<T>>) {
    Object.assign(this, data);
  }

  static from = <T>(data?: Partial<RestResponse<T>>) =>
    new RestResponse<T>(data);

  get isSuccess() {
    return this.httpCode === 200 && this.errCode === undefined;
  }

  get isFailure() {
    return !this.isSuccess;
  }

  get hasData() {
    return !!this.data;
  }
}

export type typeBackEnd = Partial<{
  api_url: string | undefined;
}>;