import { useEffect, useState } from "react";
import type { AppModel } from "../../models/App";
import App from "./App";
import CreateApp from "./CreateApp";
import mdwApi from "../../utils/mdwApi";
import { toast } from "sonner";

export default function Apps() {
    const [apps, setApps] = useState<AppModel[]>([]);

    async function fetchApps() {
        const response = await mdwApi.get("/apps/");
        if (response.status === 200) setApps(response.data);
        else console.log(response);
    }
    useEffect(() => {
        fetchApps();
    }, []);

    async function handleDelete(name: string) {
        const response = await mdwApi.delete(`/apps/${name}`);
        if (response.status === 200) {
            toast.info(`The App ${name} was deleted`);
            // handle apps
            const filteredApps = apps.filter((value) => value.name !== name);
            setApps(filteredApps);
        } else console.log(response);
    }
    // async function handleCreate(name: string, description?: string) {
    //     const content: AppModel = {
    //         name,
    //         description,
    //     };
    async function handleCreate(content: AppModel) {
        const name = content.name;
        const response = await mdwApi.post("/apps/", content);
        if (response.status === 200) {
            toast.info(`The App ${name} was created`);
            // handle apps
            setApps([...apps, {...content}]);
        } else {
            console.log(response)
            toast.error(`The App ${name} was NOT created`);
        };
    }

    const transformedApps: Required<AppModel>[] = [];

    apps.forEach((app) => {
        const transformedApp: Required<AppModel> = {
            name: app.name,
            description: app.description ? app.description : "",
            terms: app.terms ? app.terms : [],
            conclusions: app.conclusions ? app.conclusions : [],
            model: app.model ? app.model : "llama3",
            ignore_fields: app.ignore_fields ? app.ignore_fields : [],
        };
        transformedApps.push(transformedApp);
    });

    return (
        <main className="container mx-auto px-4">
            {/* create app */}
            <section className="my-5">
                {/* max-w-[700px] */}
                <h1 className="text-3xl">Create App</h1>
                <div className="w-full flex flex-col p-5">
                    {/* <CreateApp handleCreate={(name, description) => handleCreate(name, description)} /> */}
                    {/* <CreateApp handleCreate={(content) => handleCreate(content)} /> */}
                    <CreateApp handleCreate={handleCreate} />
                </div>
            </section>
            
            <hr />

            {/* all apps */}
            <section className="my-5 mb-20">
                <h1 className="text-3xl">Apps</h1>
                {/* <Apps apps={apps} /> */}
                {transformedApps.map((app) => (
                    <App key={app.name} {...app} handleDelete={() => handleDelete(app.name)} />
                ))}
            </section>
        </main>
    );
}
