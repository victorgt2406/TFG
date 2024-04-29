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
    async function handleCreate(name: string, description?: string) {
        const content: AppModel = {
            name,
            description,
        };
        const response = await mdwApi.post("/apps/", content);
        if (response.status === 200) {
            toast.info(`The App ${name} was created`);
            // handle apps
            setApps([...apps, { name }]);
        } else console.log(response);
    }

    const transformedApps: Required<AppModel>[] = [];

    apps.forEach((app) => {
        const transformedApp: Required<AppModel> = {
            name: app.name,
            description: app.description ? app.description : "",
            terms: app.terms ? app.terms : [],
            conclusions: app.conclusions ? app.conclusions : [],
            model: app.model ? app.model : "llama3",
        };
        transformedApps.push(transformedApp);
    });

    return (
        <main className="container mx-auto px-4">
            <h1 className="text-3xl">Apps</h1>
            <section className="my-5">
                {/* <Apps apps={apps} /> */}
                {transformedApps.map((app) => (
                    <App
                        key={app.name}
                        {...app}
                        handleDelete={() => handleDelete(app.name)}
                    />
                ))}
            </section>
            <section className="flex w-full justify-center mb-20">
                <div className="w-full max-w-[400px] flex flex-col">
                    <h2 className="text-2xl">Create App</h2>
                    <CreateApp
                        handleCreate={(name, description) =>
                            handleCreate(name, description)
                        }
                    />
                </div>
            </section>
        </main>
    );
}
