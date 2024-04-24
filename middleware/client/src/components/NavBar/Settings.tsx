import { Button } from "../../@shadcn/components/ui/button";
import {
    Popover,
    PopoverContent,
    PopoverTrigger,
} from "../../@shadcn/components/ui/popover";

export default function () {
    return (
        <div className="mx-2">
            <Popover>
                <PopoverTrigger>
                    <Button asChild variant="outline">
                        <i className="bi bi-gear-fill"></i>
                    </Button>
                </PopoverTrigger>
                <PopoverContent>
                    Place content for the popover here.
                </PopoverContent>
            </Popover>
        </div>
    );
}
