import request from '../utils/request';

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
