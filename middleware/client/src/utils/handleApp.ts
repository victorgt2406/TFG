const COOKIE_APP = "app";
import axios from "axios";
import Cookies from "js-cookie";
import type { AppModel } from "../models/App";

export default async function handleApp(appName: string) {
    const response = await axios.get(
        `http://localhost:3000/api/apps/${appName}`
    );
    // Check if exists
    if (response.status === 200) {
        const app: AppModel = response.data;
        Cookies.set(COOKIE_APP, app.name);
    }
}

function getAppCookie(): string | undefined {
    return Cookies.get(COOKIE_APP);
}

export { getAppCookie, COOKIE_APP };
