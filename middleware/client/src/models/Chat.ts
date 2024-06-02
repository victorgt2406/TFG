import type { LlmMessageType } from "./LlmMessage";

type ChatModel = {
    model: string;
    messages: LlmMessageType[];
    stream: boolean;
}

export type {ChatModel}