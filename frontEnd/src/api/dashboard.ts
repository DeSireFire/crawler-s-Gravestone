import { API } from "~/constants/api";
import {CONTENT_TYPE, REQUEST_HEADER, REQUEST_METHOD} from "~/constants/request";
import useHttp from "~/utils/request";
import {dashInfo} from "~/api/types/dashboard";

const { handleGet, http } = useHttp();

export const getDashInfo = () => {
    return handleGet({
        url: API.DASHBOARD.DBOARDINFO,
        method: REQUEST_METHOD.GET,
        headers: {},
    });
};