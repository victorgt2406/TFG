import type { LlmMessageType } from "./LlmMessage";

type AppModel =  {
    name: string;
    model?: string;
    description?: string;
    terms?: LlmMessageType[];
    conclusions?: LlmMessageType[];
    ignore_fields?: string[];
}

type UpdateAppModel = AppModel & {
    orig_name?: string;
}

export type { AppModel, UpdateAppModel };
