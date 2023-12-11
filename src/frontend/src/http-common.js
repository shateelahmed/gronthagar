import axios from "axios";

export default axios.create(
    {
        // baseURL: process.env.API_BASE_URL,
        baseURL: "http://localhost:8000",
        headers: {
            "Content-type": "application/json"
        }
    }
);