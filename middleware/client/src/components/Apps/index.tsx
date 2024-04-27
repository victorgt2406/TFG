import type { AppModel } from "../../models/App";
import App from "./App";

export default function Apps({ apps }: { apps: AppModel[] }) {
    const transformedApps: Required<AppModel>[] = [];
    apps.forEach((app) => {
        const transformedApp: Required<AppModel> = {
            name: app.name,
            description: app.description ? app.description : "",
            terms: app.terms ? app.terms : [],
            conclusions: app.conclusions ? app.conclusions : [],
        };
        transformedApps.push(transformedApp);
    });

    return (
        <>
            {transformedApps.map((app) => (
                <App key={app.name} {...app} />
            ))}
        </>
    );
}
