import type { ContextModel } from "./Context";

type AppModel =  {
    name: string;
    terms?: ContextModel[];
    conclusions?: ContextModel[];
}

export type { AppModel };
