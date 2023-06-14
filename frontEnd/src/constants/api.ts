export const BASE_URL =
    process.env.NODE_ENV === "development"
         ? import.meta.env.VITE_DEV_API ?? "http://192.168.16.15:50830"     // 测试环境
         : import.meta.env.VITE_PRO_API ?? "http://192.168.16.15:50830";  // 生产环境
        // ? import.meta.env.VITE_DEV_API ?? "http://localhost:50830"     // 测试环境
        // : import.meta.env.VITE_PRO_API ?? "http://localhost:50830";  // 生产环境

// console.log(import.meta.env)
// console.log("demo",import.meta.env.VITE_DEV_API)

// 用户接口
export enum ACCOUNT {
  LOGIN = "/auth_token",
}

// 任务日志
export enum WORKERLOGS {
  GETLOGS = "/get_logs",
  DELLOGS = "/del_logs",
}

// 附加功能接口
export enum EXTRALS {
  // IPINFO = "https://api.live.bilibili.com/xlive/web-room/v1/index/getIpInfo",
  IPINFO = "https://qifu-api.baidubce.com/ip/local/geo/v1/district?",
  // IPINFO = "http://ip-api.com/json",
  // IPINFO = "https://restapi.amap.com/v3/geocode/geo?address=%E8%B4%B5%E5%B7%9E%E7%9C%81%E9%BB%8E%E5%B9%B3%E5%8E%BF%E5%BE%B7%E5%87%A4%E8%A1%97%E9%81%93%E5%BC%80%E6%B3%B0%E8%B7%AF&output=json&key=3370627959554784bf205c139c12fbb",
}

// api 输出
export const API = {
  ACCOUNT,
  WORKERLOGS,
  EXTRALS,
};
