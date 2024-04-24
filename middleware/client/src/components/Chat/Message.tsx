import { useRef, useState } from "react";
import { Button } from "../../@shadcn/components/ui/button";
import {
    Card,
    CardContent,
    CardFooter,
    CardHeader,
} from "../../@shadcn/components/ui/card";
import { TextareaAuto } from "../TextareaAuto";

type MyProps = {
    role: "user" | "assistant" | "system";
    message: string;
};

function EditingMessage({
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

export default function Message({ role, message }: MyProps) {
    const [edit, setEdit] = useState(false);
    const [editedMessage, setEditedMessage] = useState(message);

    return (
        <div className={`${edit ? "w-full max-w-[800px]" : ""}`}>
            <Card
                className={`relative my-2 ${
                    !edit ? "w-full max-w-[800px]" : ""
                } ${role === "user" ? "border-primary" : ""}
            `}
            >
                <div className="pe-10">
                    <CardHeader
                        className={`py-2 px-3 capitalize flex ${
                            role === "user" ? "" : "flex-row-reverse"
                        }`}
                    >
                        {role}
                    </CardHeader>
                    <CardContent className="py-2 px-3">
                        {edit ? (
                            <EditingMessage
                                message={editedMessage}
                                setMessage={setEditedMessage}
                            />
                        ) : (
                            editedMessage
                        )}
                    </CardContent>
                </div>
                <Button
                    className="absolute bottom-0 right-0 m-1 size-8"
                    variant={edit ? "default" : "secondary"}
                    onClick={() => setEdit(!edit)}
                >
                    {edit ? (
                        <i className="bi bi-check"></i>
                    ) : (
                        <i className="bi bi-pencil-fill"></i>
                    )}
                </Button>
            </Card>
        </div>
    );
}
