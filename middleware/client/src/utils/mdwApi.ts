import axios from "axios";
const isDev = import.meta.env.DEV;

// Create an instance of axios with default properties
const mdwApi = axios.create({
    baseURL: isDev ? "http://localhost:3000/api" : "/api",
    timeout: 180 * 1000,
});

export default mdwApi;
