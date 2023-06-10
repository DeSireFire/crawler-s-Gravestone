import useHttp from "~/utils/request";

const { http } = useHttp();

// 测试用的demo请求们
export const get_ip_info = () => {
  return http({
    url: "https://api.live.bilibili.com/xlive/web-room/v1/index/getIpInfo",
    method: "get",
  });
};

export const fetchData = () => {
  return http({
    url: "http://127.0.0.1:50830/table.test",
    method: "get",
  });
};

export const fetchRedis = () => {
  return http({
    url: "http://127.0.0.1:8000/rset",
    method: "get",
  });
};

export const fetchdisc = () => {
  return http({
    url: "http://127.0.0.1:8000/rschart",
    method: "get",
  });
};

export const fetchCharts = () => {
  return http({
    url: "http://127.0.0.1:8000/rechart",
    method: "get",
  });
};

export const fetchChartss = () => {
  return http({
    url: "http://127.0.0.1:8000/recharts",
    method: "get",
  });
};
