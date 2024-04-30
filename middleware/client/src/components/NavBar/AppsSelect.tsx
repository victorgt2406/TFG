import { useEffect, useState } from "react";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "../../@shadcn/components/ui/select";
import type { AppModel } from "../../models/App";
import handleApp, { getApp } from "../../utils/handleApp";
import mdwApi from "../../utils/mdwApi";

export default function AppsSelect({className}:{className?:string}) {
    const [apps, setApps] = useState<string[]>([]);
    const [appValue, setAppValue] = useState<string | undefined>(undefined);
    useEffect(() => {
        async function loadApps() {
            const response = await mdwApi.get("/apps/");
            if (response.status === 200) {
                const data: AppModel[] = response.data;
                setApps(data.map((app) => app.name));
            }
        }
        setAppValue(getApp());
        // load all apps from api
        loadApps();
    }, []);

    return (
        <div className={`w-28 ${className}`}>
            <Select
                onValueChange={(value) => {
                    handleApp(value);
                    setAppValue(value);
                }}
                value={appValue}
                // defaultValue={defaultApp}
            >
                <SelectTrigger>
                    <SelectValue placeholder={"Apps"} />
                </SelectTrigger>
                <SelectContent>
                    {apps.map((app, index) => {
                        return (
                            <SelectItem
                                value={app}
                                key={"select-app-" + index}
                            >
                                {app}
                            </SelectItem>
                        );
                    })}
                </SelectContent>
            </Select>
        </div>
    );
}
