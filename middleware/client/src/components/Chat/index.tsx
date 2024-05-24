import { useEffect, useRef, useState } from "react";
import { ScrollArea } from "../../@shadcn/components/ui/scroll-area";
import type { LsmResponseType } from "../../models/LsmResponse";
import mdwApi from "../../utils/mdwApi";
import Input from "./Input";
import Output from "./Output";
import type { LsmMessageType } from "../../models/LsmMessage";
import { getApp } from "../../utils/handleApp";
import type { AppModel } from "../../models/App";
import type { OllamaChat } from "../../models/OllamaChat";
import type { LlmMessageType } from "../../models/LlmMessage";
import { toast } from "sonner";

export default function Chat() {
    const [messages, setMessages] = useState<LsmMessageType[]>([]);
    const scrollRef = useRef<HTMLDivElement>(null);

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
        const response = await mdwApi.post("/ollama/", body);
        if (response.status === 200) {
            console.log(response);
            const responseMsg: string = response.data.message.content;
            return responseMsg;
        } else {
            toast.error("Error when loading terms");
        }
        return undefined;
    }

    async function fetchDocs(query: string) {
        const response = await mdwApi.post("/search/", {
            query,
        });
        if (response.status === 200) {
            return response.data as any[];
        } else {
            return undefined;
        }
    }

    async function handleMessage(message: string) {
        const appName = getApp();
        const lsmResponse: LsmResponseType = {
            message,
            conclusion: "",
            docs: [],
            terms: [],
        };
        if (appName) {
            // input message
            setMessages([...messages, { message, role: "user" }, { message: "...", role: "assistant", lsmResponse }]);
            const app = await fetchApp(appName);
            const terms = app?.terms || [];
            const conclusions = app?.conclusions || [];
            const model = app?.model || "llama3";

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
            const responseDocs = (await fetchDocs(cleanTerms.join(" "))) || [];
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

    return (
        <>
            <ScrollArea ref={scrollRef}>
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
