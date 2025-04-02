import axios from "axios"

const apiUrl = import.meta.env.VITE_API_URL;
const apiVersion = import.meta.env.VITE_API_URL_VERSION;

const credentials = btoa('project1:project1');
const credentials2 = btoa('project2:project2');
const credentials3 = btoa('admin:adminpassword');

export const baseURL = `${apiUrl}${apiVersion}`;

export const headers = {
    //'Authorization': `Basic ${credentials2}`,
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'mode': 'cors',
}

export const axiosInstance = axios.create({
  baseURL,
  headers
});