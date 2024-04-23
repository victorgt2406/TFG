import {
    Popover,
    PopoverContent,
    PopoverTrigger,
} from "../../@shadcn/components/ui/popover";

export default function () {
    return (
        <Popover>
            <PopoverTrigger>
                <i className="bi bi-gear-fill"></i>
            </PopoverTrigger>
            <PopoverContent>Place content for the popover here.</PopoverContent>
        </Popover>
    );
}
