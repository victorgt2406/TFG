import type { LlmRoleType } from "./LlmRole";

type LlmMessage = {
    model?: string;
    role: LlmRoleType;
    content: string;
};
export type { LlmMessage };
