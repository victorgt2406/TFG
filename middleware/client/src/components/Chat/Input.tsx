import { useRef } from "react";
import { Textarea } from "../../@shadcn/components/ui/textarea";
import { Button } from "../../@shadcn/components/ui/button";

export default function Input() {
    const text = useRef<HTMLTextAreaElement>(null);

    const handleInput = () => {
        const textarea = text.current;
        if (textarea) {
          textarea.style.height = 'auto'; // Reset height to recalculate
          textarea.style.height = `${textarea.scrollHeight}px`;
        }
      };

    return (
        <div className="relative">
            <Textarea
                ref={text}
                onInput={handleInput}
                className="resize-none pr-10 overflow-hidden"
                placeholder="Type your message here."
            />
            <Button className="absolute bottom-0 right-0 m-1 size-8" onClick={()=>alert("hey")}><i className="bi bi-send"></i></Button>
        </div>
    );
}
