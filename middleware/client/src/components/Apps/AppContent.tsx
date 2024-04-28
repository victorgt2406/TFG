import { useState } from "react";
import { AccordionContent } from "../../@shadcn/components/ui/accordion";
import type { AppModel } from "../../models/App";
import ContextMessage from "./ContextMessage";
import type { LlmMessageType } from "../../models/LlmMessage";
import { Button } from "../../@shadcn/components/ui/button";
import { toast } from "sonner";

// type LlmMessageIndexType = LlmMessageType & { index: number };

type MyProps = {
    // app: AppModel;
    messages: LlmMessageType[];
};

export default function AppContent({ messages: defaultMessages }: MyProps) {
    const [messages, setMessages] = useState(defaultMessages);

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
            <div className="flex justify-center mt-3">
                <Button onClick={handleNewMessage}>Create New Message</Button>
            </div>
        </AccordionContent>
    );
}

// export type { LlmMessageType };
