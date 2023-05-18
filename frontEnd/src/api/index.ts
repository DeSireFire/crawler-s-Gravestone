import request from '../utils/request';

export const userLogin = (username, password) => {
    return request({
        url: 'http://127.0.0.1:8089/login',
        method: 'post',
        data: {
            username: username,
            password: password
        }
    });
};

// 测试用的demo请求们
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
