import type { LlmMessage } from "./LlmMessage";

type AppModel =  {
    name: string;
    description?: string;
    terms?: LlmMessage[];
    conclusions?: LlmMessage[];
}

export type { AppModel };
