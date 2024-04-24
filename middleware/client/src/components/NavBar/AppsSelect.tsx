import { useEffect, useState } from "react";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "../../@shadcn/components/ui/select";
import axios from "axios";
import type { AppModel } from "../../models/App";
import handleApp, { getAppCookie } from "../../utils/handleApp";

export default function AppsSelect() {
    const [apps, setApps] = useState<string[]>([]);
    const [appValue, setAppValue] = useState<string | undefined>(undefined);
    useEffect(() => {
        async function loadApps() {
            const response = await axios.get(`http://localhost:3000/api/apps/`);
            if (response.status === 200) {
                const data: AppModel[] = response.data;
                setApps(data.map((app) => app.name));
            }
        }
        setAppValue(getAppCookie());
        // load all apps from api
        loadApps();
    }, []);

    return (
        <div className="w-28 mx-2">
            <Select
                onValueChange={(value) => {
                    handleApp(value);
                    setAppValue(value);
                }}
                value={appValue}
                // defaultValue={defaultApp}
            >
                <SelectTrigger>
                    <SelectValue className="capitalize" placeholder={"Apps"} />
                </SelectTrigger>
                <SelectContent>
                    {apps.map((app, index) => {
                        return (
                            <SelectItem
                                className="capitalize"
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
