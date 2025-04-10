import axios from "axios"

const apiUrl = import.meta.env.VITE_API_URL;
const apiVersion = import.meta.env.VITE_API_URL_VERSION;

export const users = [
  //btoa('project1:project1'),
  //btoa('project2:project2'),
  //btoa('admin:adminpassword')
]

export const baseURL = `${apiUrl}${apiVersion}`;

export const axiosInstance = (user: string = users[0]) => axios.create({
  baseURL,
  headers: {
    'Authorization': `Basic ${user}`,
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'mode': 'cors'
  }
});