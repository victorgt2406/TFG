import { useState } from "react";
import { Button, buttonVariants } from "../../@shadcn/components/ui/button";
import { Card, CardContent, CardFooter, CardHeader } from "../../@shadcn/components/ui/card";
import EditingMessage from "./EditingMessage";
import type { LsmResponseType } from "../../models/LsmResponse";
import MessageFooter from "./MessageFooter";
import type { LlmRoleType } from "../../models/LlmRole";
import Markdown from "react-markdown";
import remarkGfm from 'remark-gfm'
import 'github-markdown-css'

type MyProps = {
    role: LlmRoleType;
    message: string;
    lsmResponse?: LsmResponseType;
};

export default function Message({ role, message, lsmResponse }: MyProps) {
    const [edit, setEdit] = useState(false);
    const [editedMessage, setEditedMessage] = useState(message);

    const footer = lsmResponse ? (
        <CardFooter>
            <MessageFooter {...lsmResponse} />
        </CardFooter>
    ) : (
        <></>
    );
    const messageComponent = edit ? (
        <EditingMessage message={editedMessage} setMessage={setEditedMessage} />
    ) : (
        <>
            {message === "..." ? (
                <span className={buttonVariants({ variant: "ghost" })}>
                    <i className="bi bi-arrow-clockwise animate-spin"></i>
                </span>
            ) : (
                <Markdown remarkPlugins={[remarkGfm]} className="markdown-body">{message}</Markdown>
            )}
        </>
    );

    return (
        <div className={`w-full flex ${role === "user" ? "flex-row-reverse" : "flex-row"}`}>
            <Card
                className={`
                relative max-w-[1000px] my-1 ${role === "user" ? "border-primary" : ""} ${edit ? "w-full" : ""}
            `}
            >
                <div className="pe-10">
                    <CardHeader className={`py-2 px-3 capitalize flex ${role === "user" ? "" : "flex-row-reverse"}`}>
                        {role}
                    </CardHeader>
                    <CardContent className="py-2 px-3">{messageComponent}</CardContent>
                    {footer}
                </div>
                <Button
                    className="absolute bottom-0 right-0 m-1 size-8"
                    variant={edit ? "default" : "secondary"}
                    onClick={() => setEdit(!edit)}
                >
                    {edit ? <i className="bi bi-check"></i> : <i className="bi bi-pencil-fill"></i>}
                </Button>
            </Card>
        </div>
    );
}
