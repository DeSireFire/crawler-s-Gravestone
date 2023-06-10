import { API } from "~/constants/api";
import {CONTENT_TYPE, REQUEST_HEADER, REQUEST_METHOD} from "~/constants/request";
import useHttp from "~/utils/request";

const { handleGet } = useHttp();
export const getLogs = () => {
    return handleGet({
        url: API.WORKERLOGS.GETLOGS,
        method: REQUEST_METHOD.GET,
        headers: {},
    });
};
