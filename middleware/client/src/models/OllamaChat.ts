import type { LlmMessageType } from "./LlmMessage";

type OllamaChat = {
    model: string;
    messages: LlmMessageType[];
    stream: boolean;
}

export type {OllamaChat};