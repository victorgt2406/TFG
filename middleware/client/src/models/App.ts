import type { LlmMessageType } from "./LlmMessage";

type AppModel =  {
    orig_name?: string;
    name: string;
    model?: string;
    description?: string;
    terms?: LlmMessageType[];
    conclusions?: LlmMessageType[];
    ignore_fields?: string[];
}

export type { AppModel };
