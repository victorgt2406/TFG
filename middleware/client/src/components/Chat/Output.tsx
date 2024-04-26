import type { LsmMessageType } from "../../models/LsmMessage";
import Message from "./Message";

type MyProps = {
    className?: string;
    messages: LsmMessageType[];
};

export default function ({ className, messages }: MyProps) {

    const messagesComps = messages.map((message, index)=>{
        return (<Message key={"message-"+index} {...message}/>)
    })

    return (
        <div className={`flex flex-col ${className}`}>
            {messagesComps}
        </div>
    );
}
