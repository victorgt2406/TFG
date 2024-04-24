import { useRef } from "react";
import { Textarea } from "../@shadcn/components/ui/textarea";

export default function Input() {
    const text = useRef<HTMLTextAreaElement>(null);

    const handleInput = () => {
        const textarea = text.current;
        if (textarea) {
            textarea.style.height = "auto"; // Reset height to recalculate
            textarea.style.height = `${textarea.scrollHeight}px`;
        }
    };

    return (
        <Textarea
            ref={text}
            onInput={handleInput}
            className="resize-none overflow-hidden"
            placeholder="Type your message here."
        />
    );
}
