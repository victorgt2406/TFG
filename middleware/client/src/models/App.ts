import type { LlmMessageType } from "./LlmMessage";

type AppModel =  {
    name: string;
    model?: string;
    description?: string;
    terms?: LlmMessageType[];
    conclusions?: LlmMessageType[];
}

export type { AppModel };
