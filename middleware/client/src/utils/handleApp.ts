const KEY_APP = "app";
import { toast } from "sonner";
import mdwApi from "./mdwApi";

export default async function handleApp(appName: string) {
    localStorage.setItem(KEY_APP, appName);
    const lastAppName = getAppName();
    
    const response = await mdwApi(`/apps/${appName}`);
    // Check if exists
    if (response.status !== 200 && response.data.name !== appName) {
        toast.error("Error handling app change");
        if(lastAppName) {
            localStorage.setItem(KEY_APP, lastAppName)
        };
    }
}

function getAppName(): string | undefined {
    const appName = localStorage.getItem(KEY_APP)
        ? localStorage.getItem(KEY_APP)!
        : undefined;
    return appName;
}

export { getAppName, KEY_APP as GLOBAL_APP };
