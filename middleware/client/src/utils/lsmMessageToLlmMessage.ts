import type { LlmMessageType } from "../models/LlmMessage";
import type { LsmMessageType } from "../models/LsmMessage";


export default function lsmMessageToLlmMessage(message:LsmMessageType):LlmMessageType{
    return {
        role: message.role,
        content: message.message
    };
}