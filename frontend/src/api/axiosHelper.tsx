import axios from "axios"

const apiUrl = import.meta.env.VITE_API_URL;
const apiVersion = import.meta.env.VITE_API_URL_VERSION;

export const users = [
  btoa('name:name'),
]

export const baseURL = `${apiUrl}${apiVersion}`;

export const axiosInstance = (user: string = users[0]) => axios.create({
  baseURL,
  headers: {
    //'Authorization': `Basic ${user}`,
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'mode': 'cors'
  }
});