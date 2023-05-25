import request from '../utils/request';
import LoginParam from '../types/account';


export const userLogin = (payload: LoginParam) => {
    return $fetch(
        request, {
            url: 'http://127.0.0.1:6701/login',
            method: 'post',
            data: payload,
        }
    )
}


// 测试用的demo请求们
export const get_ip_info = () => {
    return request({
        url: 'https://api.live.bilibili.com/xlive/web-room/v1/index/getIpInfo',
        method: 'get'
    });
}

export const fetchData = () => {
    return request({
        url: 'http://127.0.0.1:8000/table.test',
        method: 'get'
    });
};

export const fetchRedis = () => {
    return request({
        url: 'http://127.0.0.1:8000/rset',
        method: 'get'
    });
};

export const fetchdisc = () => {
    return request({
        url: 'http://127.0.0.1:8000/rschart',
        method: 'get'
    });
};

export const fetchCharts = () => {
    return request({
        url: 'http://127.0.0.1:8000/rechart',
        method: 'get'
    });
};

export const fetchChartss = () => {
    return request({
        url: 'http://127.0.0.1:8000/recharts',
        method: 'get'
    });
};
