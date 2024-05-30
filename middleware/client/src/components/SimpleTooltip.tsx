import type React from "react";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "../@shadcn/components/ui/tooltip";

type MyProps = {
    children?: React.ReactNode;
    tip?: React.ReactNode;
};

export default function SimpleTooltip({ children, tip }: MyProps) {
    return (
        <TooltipProvider>
            <Tooltip>
                <TooltipTrigger>{children}</TooltipTrigger>
                <TooltipContent>{tip}</TooltipContent>
            </Tooltip>
        </TooltipProvider>
    );
}
