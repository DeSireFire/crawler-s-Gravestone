export const BASE_URL =
    process.platform.includes('win')
        ? import.meta.env.VITE_DEV_API ?? "http://127.0.0.1:50830"     // 测试环境
        : import.meta.env.VITE_PRO_API ?? "http://192.168.16.15:50830" // 生产环境
if (process.platform.includes('win')) {
  console.log(process.platform, "检测为windows系统，切换与后端的交互为localhost！")
}
if (process.platform.includes('linux')) {
  console.log(process.platform, "检测为linux系统，切换与后端的交互为localhost！")
}
// console.log(process.platform.includes('win'))
// console.log(import.meta.env)
// console.log("demo",import.meta.env.VITE_DEV_API)

// 用户接口
export enum ACCOUNT {
  LOGIN = "/auth_token",
  ADDUSER = "/add_user",
  EDITUSER = "/edit_user",
  DELUSER = "/del_user",
  GETUSERS = "/get_users",
}

// 系统首页
export enum DASHBOARD {
  DBOARDINFO = "/dboard_info",
}

// 任务日志
export enum WORKERLOGS {
  GETLOGS = "/get_logs",
  GETLOGCONTENT = "/get_log_content",
  DELLOGS = "/del_logs",
}

// 项目管理
export enum PROJECTS {
  GETPROJECTS = "/get_projects",
  GETPROJECTSNAMES = "/get_projects_names",
  GETPROJECT = "/get_project",
  ADDPROJECT = "/add_project",
  DELPROJECT = "/del_project",
  UPDATEPROJECT = "/update_project",

  GETWORKERS = "/get_workers",
  GETWORKER = "/get_worker",
  ADDWORKERS = "/add_workers",
  DELWORKERS = "/del_workers",
  UPDATEWORKERS = "/update_workers",

  GETJOBS = "/get_jobs",
  DELJOBS = "/del_jobs",

  GETLOG = "/get_log",

  GETPTASKS = "/get_ptasks",
}

// 告警管理
export enum ALARMS {
  // 添加删除告警器
  GETALARMERS = "/get_alarmers",
  ADDALARMERS = "/add_alarmers",
  DELALARMERS = "/del_alarmers",

  // 注册告警服务
  GETALARMERJOBS = "/get_alarmer_jobs",
  UPDATEALARMERJOBS = "/update_alarmer_jobs",
  ADDALARMERJOBS = "/add_alarmer_jobs",
  DELALARMERJOBS = "/del_alarmer_jobs",
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
  DASHBOARD,
  WORKERLOGS,
  EXTRALS,
  PROJECTS,
  ALARMS,
};
