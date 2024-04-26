import { useEffect, useRef, useState } from "react";
import { ScrollArea } from "../../@shadcn/components/ui/scroll-area";
import type { LsmResponseType } from "../../models/LsmResponse";
import mdwApi from "../../utils/mdwApi";
import Input from "./Input";
import Output from "./Output";
import type { LsmMessageType } from "../../models/LsmMessage";

export default function Chat() {
    const [messages, setMessages] = useState<LsmMessageType[]>([]);
    const scrollRef = useRef<HTMLDivElement>(null);

    async function handleMessage(message: string) {
        console.log(message);
        setMessages([
            ...messages,
            { message, role: "user" },
        ]);
        const response = await mdwApi.post("/chat/", {
            message,
        });
        if (response.status === 200) {
            const lsmResponse: LsmResponseType = response.data;
            const assistantMessage = lsmResponse.conclusion;
            setMessages([
                ...messages,
                { message, role: "user" },
                { message: assistantMessage, lsmResponse, role: "assistant" }
            ]);
            // console.log(response.data)
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
                <section className="flex justify-center">
                    <Output
                        className="my-1 container p-0 min-h-[calc(100vh-106px)]"
                        messages={messages}
                    />
                </section>
            </ScrollArea>
            <section className="container mt-1 mb-2 w-full p-0">
                <Input handleMessage={handleMessage} />
            </section>
        </>
    );
}
