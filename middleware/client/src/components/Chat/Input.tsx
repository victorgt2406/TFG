import { useRef, useState } from "react";
import { Textarea } from "../../@shadcn/components/ui/textarea";
import { Button } from "../../@shadcn/components/ui/button";

type MyProps = {
    handleMessage: (message: string) => Promise<void>;
};

export default function Input({ handleMessage }: MyProps) {
    const [isLoading, setLoading] = useState(false);
    const text = useRef<HTMLTextAreaElement>(null);

    const handleInput = () => {
        const textarea = text.current;
        if (textarea) {
            textarea.style.height = "auto"; // Reset height to recalculate
            textarea.style.height = `${textarea.scrollHeight}px`;
        }
    };

    async function handleClick() {
        const message = text.current?.value;
        if (message) {
            setLoading(true);
            await handleMessage(message);
            setLoading(false);
        }
    }

    return (
        <div className="relative">
            <Textarea
                ref={text}
                onInput={handleInput}
                className="resize-none pr-10 overflow-hidden"
                placeholder="Type your message here."
            />
            <Button
                disabled={isLoading}
                className="absolute bottom-0 right-0 m-1 size-8"
                onClick={handleClick}
            >
                <i
                    className={`bi ${
                        isLoading
                            ? "bi-arrow-clockwise animate-spin"
                            : "bi-send"
                    }`}
                ></i>
            </Button>
        </div>
    );
}
