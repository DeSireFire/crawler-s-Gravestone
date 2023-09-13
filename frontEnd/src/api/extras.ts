// import { IpData } from "~/api/types/extras";
import { API } from "~/constants/api";
import {CONTENT_TYPE, REQUEST_HEADER, REQUEST_METHOD} from "~/constants/request";
import useHttp from "~/utils/request";

const { http } = useHttp();

// export const ipInfo = () => {
//     REQUEST_HEADER
//     const temp = request<IpData>({
//         url: API.EXTRALS.IPINFO,
//         headers: {
//         },
//     });
//     console.log("temp", temp)
//     return temp
// };

export const ipInfo = () => {
    return http({
        url: API.EXTRALS.IPINFO,
        method: REQUEST_METHOD.GET,
        headers: {
        },
    });
};
