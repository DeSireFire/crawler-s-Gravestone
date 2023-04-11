import request from '../utils/request';

export const fetchData = () => {
    return request({
        url: 'http://127.0.0.1:8000/table.test',
        method: 'get'
    });
};
