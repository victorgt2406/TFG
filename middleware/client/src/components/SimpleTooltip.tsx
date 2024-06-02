import type React from "react";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "../@shadcn/components/ui/tooltip";
import { forwardRef } from "react";

type MyProps = {
    children?: React.ReactNode;
    tip?: React.ReactNode;
};

// export default function SimpleTooltip({ children, tip }: MyProps) {
//     return (
//         <TooltipProvider>
//             <Tooltip>
//                 <TooltipTrigger asChild={true}>{children}</TooltipTrigger>
//                 <TooltipContent>{tip}</TooltipContent>
//             </Tooltip>
//         </TooltipProvider>
//     );
// }


const SimpleTooltip = forwardRef<HTMLDivElement, MyProps>(({ children, tip }, ref) => {
    return (
        <TooltipProvider>
            <Tooltip>
                <TooltipTrigger asChild>
                    <div ref={ref}>{children}</div>
                </TooltipTrigger>
                <TooltipContent>{tip}</TooltipContent>
            </Tooltip>
        </TooltipProvider>
    );
});

SimpleTooltip.displayName = "SimpleTooltip";

export default SimpleTooltip;

