import * as React from "react";
import { cn } from "../@shadcn/lib/utils"; // Verify the correct path and spelling.

export interface TextareaProps
    extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {}

const TextareaAuto = React.forwardRef<HTMLTextAreaElement, TextareaProps>(
    ({ className, ...props }, ref) => {
        const textareaRef =
            ref as React.MutableRefObject<HTMLTextAreaElement | null>;

        const handleHeight = () => {
            const textarea = textareaRef.current;
            if (textarea) {
                textarea.style.height = "auto";
                textarea.style.height = `${textarea.scrollHeight}px`;
            }
        };

        React.useEffect(() => {
            handleHeight();
        }, [props.defaultValue]);

        return (
            <textarea
                className={cn(
                    "flex w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 resize-none overflow-hidden",
                    className
                )}
                ref={textareaRef}
                onInput={handleHeight}
                // when defaultValue
                {...props}
            />
        );
    }
);
TextareaAuto.displayName = "Textarea";

export { TextareaAuto };
