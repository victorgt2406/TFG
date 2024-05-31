import { toast } from "sonner";
import type { LlmMessageType } from "../models/LlmMessage";
import type { LlmChat } from "../models/LlmChat";
import mdwApi from "./mdwApi";

export default async function handleLlm(messages: LlmMessageType[], model: string = "llama3", stream: boolean=false){
    const body: LlmChat = {
        model,
        messages,
        stream
    };
    // console.log(body);
    const response = await mdwApi.post("/llm/", body);
    if (response.status === 200) {
        // console.log(response);
        const responseMsg: string = response.data.message.content;
        return responseMsg;
    } else {
        toast.error("Error when loading terms");
    }
    return undefined;
}