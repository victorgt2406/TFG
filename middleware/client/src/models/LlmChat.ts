import type { LlmMessageType } from "./LlmMessage";

type LlmChat = {
    model: string;
    messages: LlmMessageType[];
    stream: boolean;
}

export type {LlmChat};