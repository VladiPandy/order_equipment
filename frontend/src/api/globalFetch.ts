import { axiosInstance } from "./axiosHelper";
import { onError } from "../utils/toast";

const user = localStorage.getItem("user") || undefined

// eslint-disable-next-line
export const globalGet = (path: string, callback: any, body: any = {}) => {
    console.log(`Start get ${path}`)
    axiosInstance(user).request({
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

    axiosInstance(user).request({
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

    axiosInstance(user).request({
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