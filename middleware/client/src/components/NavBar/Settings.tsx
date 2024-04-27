import { Button, buttonVariants } from "../../@shadcn/components/ui/button";
import {
    Popover,
    PopoverContent,
    PopoverTrigger,
} from "../../@shadcn/components/ui/popover";

export default function ({className}:{className?:string}) {
    return (
        <div className={className}>
            <Popover>
                <PopoverTrigger>
                    <Button asChild variant="outline">
                        <i className="bi bi-gear-fill"></i>
                    </Button>
                </PopoverTrigger>
                <PopoverContent className="w-fit me-4">
                    <a href="/apps" className={buttonVariants({ variant: "link" })}>
                        <i className="bi bi-chat-square-text-fill me-2"></i>
                        <span>Advanced Apps config</span>
                    </a>
                </PopoverContent>
            </Popover>
        </div>
    );
}
