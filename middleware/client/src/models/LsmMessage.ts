import type { LsmResponseType } from "./LsmResponse";
import type { LlmRoleType } from "./LlmRole";

type LsmMessageType = {
    role: LlmRoleType;
    message: string;
    lsmResponse?: LsmResponseType;
};

export type { LsmMessageType };
