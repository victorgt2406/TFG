import type { LlmRoleType } from "./LlmRole";

type LlmMessageType = {
    role: LlmRoleType;
    content: string;
};
export type { LlmMessageType };
