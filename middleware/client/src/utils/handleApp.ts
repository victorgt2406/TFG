const KEY_APP = "app";
import { toast } from "sonner";
import mdwApi from "./mdwApi";
import useStore from "./zustand";

export default async function handleApp(appName: string) {
    const setApp = useStore((state) => state.setApp)
    const lastAppName = getAppName();
    localStorage.setItem(KEY_APP, appName);
    setApp(appName);
    
    const response = await mdwApi(`/apps/${appName}`);
    // Check if exists
    if (response.status !== 200 && response.data.name !== appName) {
        toast.error("Error handling app change");
        if(lastAppName) {
            localStorage.setItem(KEY_APP, lastAppName)
            setApp(lastAppName);
        };
    }
}

function getAppName(): string | undefined {
    // return Cookies.get(GLOBAL_APP);
    const appName = localStorage.getItem(KEY_APP)
        ? localStorage.getItem(KEY_APP)!
        : undefined;
    return appName;
}

export { getAppName, KEY_APP as GLOBAL_APP };
