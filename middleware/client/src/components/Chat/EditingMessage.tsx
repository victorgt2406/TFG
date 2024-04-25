import { useRef } from "react";
import { TextareaAuto } from "../TextareaAuto";


export default function EditingMessage({
    message,
    setMessage,
}: {
    message: string;
    setMessage: (msg: string) => void;
}) {
    const ref = useRef<HTMLTextAreaElement>(null);
    const handleChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
        setMessage(event.target.value);
    };
    return (
        <TextareaAuto
            ref={ref}
            defaultValue={message}
            onChange={handleChange}
        />
    );
}