import type { AppModel } from "../../models/App";
import App from "./App";


export default function Apps({apps}:{apps:AppModel[]}){
    return (
        <>{apps.map((app: AppModel) => <App {...app} />)}</>
    );
}