const GLOBAL_APP = "app";
import { toast } from "sonner";
// import Cookies from "js-cookie";
import type { AppModel } from "../models/App";
import mdwApi from "./mdwApi";

export default async function handleApp(appName: string) {
    const response = await mdwApi(`/apps/${appName}`);
    // Check if exists
    if (response.status === 200 && response.data.name === appName) {
        // const app: AppModel = response.data;
        // Cookies.set(GLOBAL_APP, appName);
        localStorage.setItem(GLOBAL_APP, appName);
    }
    else{
        toast.error("Error handling app change")
    }
}

function getApp(): string | undefined {
    // return Cookies.get(GLOBAL_APP);
    const app = localStorage.getItem(GLOBAL_APP)
        ? localStorage.getItem(GLOBAL_APP)!
        : undefined;
    return app;
}

export { getApp, GLOBAL_APP };
