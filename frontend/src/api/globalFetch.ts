import { axiosInstance } from "./axiosHelper";
import { onError } from "../utils/toast";

// eslint-disable-next-line
export const globalGet = (path: string, callback: any, body: any = {}) => {
    console.log(`Start get ${path}`)
    axiosInstance.request({
        method: 'get',
        url: path, 
        data: body,
        withCredentials: true
    })
    .then((res) => {
        callback(res.data)
    })
    .catch((error) => {
        onError(error);
    });
};

// eslint-disable-next-line
export const globalPost = (path: string, callback: any, body: any) => {
    console.log(`Start post ${path}`, body)

    axiosInstance.request({
        method: 'post',
        url: path, 
        data: body,
        withCredentials: true
    })
    .then((res) => {
        callback(res.data)
    })
    .catch((error) => {
        onError(error);
    });
};

// eslint-disable-next-line
export const globalDelete = (path: string, callback: any, body: any) => {
    console.log(`Start delete ${path}`, body)

    axiosInstance.request({
        method: 'delete',
        url: path, 
        data: body,
        withCredentials: true
    })
    .then((res) => {
        callback(res.data)
    })
    .catch((error) => {
        onError(error);
    });
};