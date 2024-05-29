import { useEffect, useRef, useState } from "react";
import { ScrollArea } from "../../@shadcn/components/ui/scroll-area";
import type { LsmResponseType } from "../../models/LsmResponse";
import mdwApi from "../../utils/mdwApi";
import Input from "./Input";
import Output from "./Output";
import type { LsmMessageType } from "../../models/LsmMessage";
import { getAppName } from "../../utils/setAppName";
import type { AppModel } from "../../models/App";
import type { OllamaChat } from "../../models/OllamaChat";
import type { LlmMessageType } from "../../models/LlmMessage";
import { toast } from "sonner";

export default function Chat() {
    const [messages, setMessages] = useState<LsmMessageType[]>([]);
    const scrollRef = useRef<HTMLDivElement>(null);
    const [app, setApp] = useState<AppModel | undefined>(undefined);

    useEffect(()=>{
        async function loadApp(){
            const appName = getAppName()
            if(appName)
            setApp(await fetchApp(appName))
        }
        loadApp();
    },[])

    // async function handleMessage(message: string) {
    //     console.log(message);
    //     setMessages([
    //         ...messages,
    //         { message, role: "user" },
    //     ]);
    //     const response = await mdwApi.post("/chat/", {
    //         message,
    //     });
    //     if (response.status === 200) {
    //         const lsmResponse: LsmResponseType = response.data;
    //         const assistantMessage = lsmResponse.conclusion;
    //         setMessages([
    //             ...messages,
    //             { message, role: "user" },
    //             { message: assistantMessage, lsmResponse, role: "assistant" }
    //         ]);
    //         // console.log(response.data)
    //     }
    // }

    async function fetchApp(appName: string) {
        const response = await mdwApi.get(`/apps/${appName}`);
        if (response.status === 200) {
            return response.data as AppModel;
        } else {
            return undefined;
        }
    }

    async function queryLLM(model: string, messages: LlmMessageType[], stream: boolean) {
        const body: OllamaChat = {
            model,
            messages,
            stream,
        };
        console.log(body);
        const response = await mdwApi.post("/llm/", body);
        if (response.status === 200) {
            console.log(response);
            const responseMsg: string = response.data.message.content;
            return responseMsg;
        } else {
            toast.error("Error when loading terms");
        }
        return undefined;
    }

    async function fetchDocs(appName:string, query: string, ignore_fields:string[]) {
        const response = await mdwApi.post(`/search/${appName}`, {
            query,
            ignore_fields
        });
        if (response.status === 200) {
            return response.data as any[];
        } else {
            return undefined;
        }
    }

    async function handleMessage(message: string) {
        // const appName = getApp();
        const lsmResponse: LsmResponseType = {
            message,
            conclusion: "",
            docs: [],
            terms: [],
        };
        if (app) {
            // input message
            setMessages([...messages, { message, role: "user" }, { message: "...", role: "assistant", lsmResponse }]);
            // const app = await fetchApp(appName);
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
            
            const responseTerms = (await queryLLM(model, terms, false)) || "";
            const cleanTerms = responseTerms.replace(" ", "").split(",");
            lsmResponse.terms = cleanTerms;
            setMessages([...messages, { message, role: "user" }, { message: "...", role: "assistant", lsmResponse }]);

            // Getting docs
            const responseDocs = (await fetchDocs(appName, cleanTerms.join(" "), ignore_fields)) || [];
            lsmResponse.docs = responseDocs;
            setMessages([
                ...messages,
                { message, role: "user" },
                { message: "loading response", role: "assistant", lsmResponse },
            ]);

            // Getting conclusion
            conclusions.push({
                role: "user",
                content: `User: ${message}\nTerms: ${JSON.stringify(cleanTerms)}\nDocs: ${JSON.stringify(
                    responseDocs
                )}`,
            });
            const responseConclusion = (await queryLLM(model, conclusions, false)) || "";
            lsmResponse.conclusion = responseConclusion;
            setMessages([
                ...messages,
                { message, role: "user" },
                { message: responseConclusion, role: "assistant", lsmResponse },
            ]);
            toast("Question answered " + responseConclusion);
        }
    }

    useEffect(() => {
        if (scrollRef.current) {
            const scrollElement = scrollRef.current;
            scrollElement.scrollTop = scrollElement.scrollHeight;
        }
    }, [messages]);

    const appName = app?.name || "Select an application!!"
    const appDescription = app?.description || "You can create a new one in the app section."

    return (
        <>
            <ScrollArea ref={scrollRef}>
                <section className="flex  flex-col justify-center items-center">
                    <h1 className="mb-4 text-4xl font-semibold uppercase">{appName}</h1>
                    <p className="text-lg">{appDescription}</p>
                </section>
                <section className="flex justify-center px-4">
                    <Output className="my-1 container p-0 min-h-[calc(100vh-106px)]" messages={messages} />
                </section>
            </ScrollArea>
            <section className="container mt-1 mb-2 w-full px-4">
                <Input handleMessage={handleMessage} />
            </section>
        </>
    );
}
