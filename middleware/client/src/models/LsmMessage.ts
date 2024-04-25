import type { LsmResponseType } from "./LsmResponse";
import type { LsmRoleType } from "./LsmRole";

type LsmMessageType = {
    role: LsmRoleType;
    message: string;
    lsmResponse?: LsmResponseType;
};

export type { LsmMessageType };
