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
import { Textarea } from "../../@shadcn/components/ui/textarea";
import UploadData from "./UploadDataButton";

type MyProps = {
    messages: LlmMessageType[];
    setMessages: React.Dispatch<React.SetStateAction<LlmMessageType[]>>;
    name: string;
    model?: string;
    section: "terms" | "conclusions";
};

export default function AppContent({ messages, setMessages, model, name }: MyProps) {
    const testTextRef = useRef<HTMLTextAreaElement>(null);
    const [isTesting, setTesting] = useState(false);
    const [testResponse, setTestResponse] = useState("");

    function handleNewMessage() {
        setMessages((prevMessages) => {
            const newMessage: LlmMessageType = {
                role: "user",
                content: "",
            };
            return [...prevMessages, newMessage];
        });
    }

    async function handleTest() {
        setTesting(true);
        setTestResponse("");
        const newMessage: LlmMessageType = {
            role: "user",
            content: testTextRef.current?.value ? testTextRef.current?.value : "",
        };
        const chat: ChatModel = {
            model: model ? model : "llama3",
            messages: [...messages, newMessage],
            stream: false,
        };
        const response = await mdwApi.post("/ollama/", chat);
        const message = response.data.message.content;
        console.log(response);
        toast.info(`The LLM response: ${message}`);
        setTesting(false);
        setTestResponse(message);
    }

    function handleMove(origIndex: number, move: number) {
        const index = origIndex + move;
        if (index >= 0 && index < messages.length) {
            setMessages((prevMessages) => {
                const newMessages = [...prevMessages];
                const temp = newMessages[origIndex];
                newMessages[origIndex] = newMessages[index];
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

    function handleUpdate(index: number, newMessage: LlmMessageType) {
        setMessages((prevMessages) => {
            const newMessages = [...prevMessages];
            newMessages[index] = newMessage;
            // console.log([...newMessages]);
            return newMessages;
        });
    }

    function OpenSearchTest() {}

    // async function handleUploadData(filename: string, data: string) {
    //     const formData = new FormData();
    //     const blobData = new Blob([data], { type: "text/plain" });

    //     formData.append("file", blobData, filename);

    //     try {
    //         const response = await mdwApi.post(`/apps/upload/${name}`, formData, {
    //             headers: {
    //                 "Content-Type": "multipart/form-data",
    //             },
    //         });
    //         console.log(response)
    //         toast(`Uploaded ${response.data} documents.`)
    //     } catch (error) {
    //         toast("Error uploading file")
    //         // console.error("Error uploading file:", error.response ? error.response.data : error.message);
    //     }
    // }

    return (
        <AccordionContent className="p-2">
            {messages.map((msg, index) => (
                <ContextMessage
                    handleDelete={handleDelete}
                    key={index}
                    role={msg.role}
                    content={msg.content}
                    index={index}
                    handleUpdate={handleUpdate}
                    handleMove={handleMove}
                />
            ))}
            <div className="mt-8">
                <div className="flex justify-center mt-2">
                    {/* add data */}
                    {/* <UploadData handleUploadData={handleUploadData} className="p-7" variant={"secondary"}/> */}
                    {/* Create new message */}
                    <Button onClick={handleNewMessage} className="p-7 ms-2">
                        New message
                        <i className="bi bi-plus"></i>
                        <i className=" bi bi-chat-left-text-fill"></i>
                    </Button>
                </div>
                <div className="flex justify-center items-center my-2">
                    <TextareaAuto ref={testTextRef} placeholder="Test message" />
                    <Textarea
                        className="resize-none overflow-hidden mx-2 disabled:opacity-100 max-w-[300px]"
                        value={testResponse}
                        placeholder="response"
                        disabled
                    ></Textarea>
                    {/* Test message */}
                    <Button onClick={handleTest} className="me-2 p-7" variant={"secondary"} disabled={isTesting}>
                        Test <i className={`ms-2 bi ${isTesting ? "bi-arrow-clockwise animate-spin" : "bi-send"}`}></i>
                    </Button>
                </div>
            </div>
        </AccordionContent>
    );
}
