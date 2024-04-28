import { useRef, useState } from "react";
import { AccordionContent } from "../../@shadcn/components/ui/accordion";
import type { AppModel } from "../../models/App";
import ContextMessage from "./ContextMessage";
import type { LlmMessageType } from "../../models/LlmMessage";
import { Button } from "../../@shadcn/components/ui/button";
import { toast } from "sonner";
import { TextareaAuto } from "../TextareaAuto";
import mdwApi from "../../utils/mdwApi";
import type { ChatModel } from "../../models/Chat";

type MyProps = {
    messages: LlmMessageType[];
    setMessages: React.Dispatch<React.SetStateAction<LlmMessageType[]>>;
    name: string;
    model?: string;
};

export default function AppContent({ messages, setMessages, model, name }: MyProps) {
    const testTextRef = useRef<HTMLTextAreaElement>(null);
    const [isTesting, setTesting] = useState(false);


    function handleNewMessage() {
        setMessages((prevMessages) => {
            const newMessage: LlmMessageType = {
                role: "user",
                content: ""
            };
            // console.log([...prevMessages, newMessage]);
            return [...prevMessages, newMessage];
        });
        // console.log(newMessages)
    }

    async function handleTest() {
        setTesting(true);
        const newMessage: LlmMessageType = {
            role: "user",
            content: testTextRef.current?.value?testTextRef.current?.value:""
        }
        const chat:ChatModel = {
            model: model?model:"llama3",
            messages : [...messages, newMessage],
            stream: false
        }
        const response = await mdwApi.post("/ollama/",chat)
        const message = response.data.message.content;
        console.log(response)
        toast.info(`The LLM response: ${message}`)
        setTesting(false);
    }

    function handleMove(origIndex: number, move: number) {
        const index = origIndex + move;
        if (index >= 0 && index < messages.length) {
            setMessages((prevMessages) => {
                const newMessages = [...prevMessages];
                const temp = newMessages[origIndex]
                newMessages[origIndex] = newMessages[index]
                newMessages[index] = temp;
                // console.log([...newMessages]);
                return newMessages;
            });
        }
    }

    function handleDelete(index: number) {
        const newMessages = [...messages];
        newMessages.splice(index);
        toast.warning("Message deleted");
        setMessages(newMessages);
        // console.log([...newMessages]);
    }

    function handleUpdate(index:number, newMessage: LlmMessageType) {
        setMessages((prevMessages) => {
            const newMessages = [...prevMessages];
            newMessages[index] = newMessage;
            // console.log([...newMessages]);
            return newMessages;
        });
    }

    return (
        <AccordionContent className="p-2">
            {messages
                .map((msg, index) => {
                    // console.log(msg);
                    return (
                        <ContextMessage
                            handleDelete={handleDelete}
                            key={index}
                            role={msg.role}
                            content={msg.content}
                            index={index}
                            handleUpdate={handleUpdate}
                            handleMove={handleMove}
                        />
                    );
                })}
            <div className="flex justify-center items-center mt-3">
                <TextareaAuto ref={testTextRef} className="me-2"/>
                <Button onClick={handleTest} className="me-2 p-7" variant={"outline"} disabled={isTesting}>Test <i className={`ms-2 bi ${isTesting?"bi-arrow-clockwise animate-spin":"bi-send"}`}></i></Button>
                <Button onClick={handleNewMessage} className="p-7"><i className="bi bi-plus"></i><i className=" bi bi-chat-left-text-fill"></i></Button>
            </div>
        </AccordionContent>
    );
}
