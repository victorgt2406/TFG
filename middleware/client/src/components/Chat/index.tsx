import { useEffect, useRef, useState } from "react";
import { ScrollArea } from "../../@shadcn/components/ui/scroll-area";
import type { LsmResponseType } from "../../models/LsmResponse";
import mdwApi from "../../utils/mdwApi";
import Input from "./Input";
import Output from "./Output";
import type { LsmMessageType } from "../../models/LsmMessage";
import type { AppModel } from "../../models/App";
import { toast } from "sonner";
import { globalAppName } from "../../utils/globals";
import { useStore } from "@nanostores/react";
import handleLlm from "../../utils/handleLlm";
import stringToTerms from "../../utils/stringToTerrms";
import handleSearch from "../../utils/handleSearch";
import createConclusionQuery from "../../utils/createConclusionQuery";
import type { LlmMessageType } from "../../models/LlmMessage";
import lsmMessageToLlmMessage from "../../utils/lsmMessageToLlmMessage";

export default function Chat() {
    const [messages, setMessages] = useState<LsmMessageType[]>([]);
    const scrollRef = useRef<HTMLDivElement>(null);
    const [app, setApp] = useState<AppModel | undefined>(undefined);

    const appName = app?.name || "Select an App!";
    const gAppName = useStore(globalAppName);
    const appDescription = app?.description || "";

    useEffect(() => {
        async function loadApp() {
            if (gAppName) setApp(await fetchApp(gAppName));
        }
        loadApp();
    }, [gAppName]);

    async function fetchApp(appName: string) {
        const response = await mdwApi.get(`/apps/${appName}`);
        if (response.status === 200) {
            return response.data as AppModel;
        } else {
            return undefined;
        }
    }

    async function handleMessage(message: string) {
        const lsmResponse: LsmResponseType = {
            message,
            conclusion: "...",
            docs: [],
            terms: [],
        };
        console.log(messages)
        if (messages.length < 2 && app) {
            // input message
            setMessages([...messages, { message, role: "user" }, { message: "...", role: "assistant", lsmResponse }]);
            // get last config of the app
            const app = await fetchApp(appName);
            const terms = app?.terms || [];
            const conclusions = app?.conclusions || [];
            const model = app?.model || "llama3";
            const ignore_fields = app?.ignore_fields || [];

            console.log("APP data", app);

            // Getting terms
            terms.push({
                role: "user",
                content: message,
            });
            const responseTerms = (await handleLlm(terms, model, false)) || "";
            const cleanTerms = stringToTerms(responseTerms);
            lsmResponse.terms = cleanTerms;
            setMessages([...messages, { message, role: "user" }, { message: "...", role: "assistant", lsmResponse }]);
            toast.info(`Terms loaded.<br>${responseTerms}`)

            // Getting docs
            const responseDocs = (await handleSearch(appName!, cleanTerms.join(" "), ignore_fields)) || [];
            lsmResponse.docs = responseDocs;
            setMessages([...messages, { message, role: "user" }, { message: "...", role: "assistant", lsmResponse }]);
            toast.info(`Documents loaded.`)

            // Getting conclusion
            conclusions.push({
                role: "user",
                content: createConclusionQuery(message, responseDocs)
            });
            // const responseConclusion = (await queryLLM(model, conclusions, false)) || "";
            const responseConclusion = (await handleLlm(conclusions, model, false)) || "";
            lsmResponse.conclusion = responseConclusion;
            setMessages([
                ...messages,
                { message, role: "user" },
                { message: responseConclusion, role: "assistant", lsmResponse },
            ]);
            // toast("Question answered " + responseConclusion);
        }
        else if(app){
            setMessages([
                ...messages,
                { message, role: "user" },
                { message: "...", role: "assistant"},
            ]);
            const model = app?.model || "llama3";
            const llmMessages:LlmMessageType[] = messages.map(lsmMessageToLlmMessage);
            llmMessages.push({
                role: "user",
                content: message,
            });
            const llmResponse = (await handleLlm(llmMessages, model, false)) || "";
            
            lsmResponse.conclusion = llmResponse;
            setMessages([
                ...messages,
                { message, role: "user" },
                { message: llmResponse, role: "assistant"},
            ]);
        }
    }

    useEffect(() => {
        if (scrollRef.current) {
            const scrollElement = scrollRef.current;
            scrollElement.scrollTop = scrollElement.scrollHeight;
        }
    }, [messages]);
    return (
        <>
            <ScrollArea ref={scrollRef}>
                <section className="flex  flex-col justify-center items-center">
                    <h1 className="mb-4 text-4xl font-semibold uppercase">{appName}</h1>
                    <p className="text-lg">{appDescription}</p>
                </section>
                <section className="flex justify-center px-4">
                    <Output className="my-1 container p-0 min-h-[calc(100vh-218px)]" messages={messages} />
                </section>
            </ScrollArea>
            <section className="container mt-1 mb-2 w-full px-4">
                <Input handleMessage={handleMessage} />
            </section>
        </>
    );
}
