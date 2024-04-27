import type { AppModel } from "../../models/App";
import App from "./App";

export default function Apps({ apps }: { apps: AppModel[] | undefined }) {

    const components = apps? apps.map((app: AppModel) => <App key={app.name} {...app} />) : <></>
    
    return (
        <>{components}</>
    )
}
