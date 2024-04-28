import { useRef, useState } from "react";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "../../@shadcn/components/ui/select";
import type { LlmRoleType } from "../../models/LlmRole";
import { TextareaAuto } from "../TextareaAuto";
import { Button } from "../../@shadcn/components/ui/button";
import type { LlmMessageType } from "../../models/LlmMessage";
// import type { LlmMessageIndexType } from "./AppContent";

type MyProps = LlmMessageType & {
    index: number;
    handleUpdate: (index: number, content: LlmMessageType) => void;
    handleDelete: (index: number) => void;
    handleMove: (index: number, move: number) => void;
};

export default function ContextMessage({
    role,
    content,
    index,
    handleUpdate,
    handleMove,
    handleDelete,
}: MyProps) {
    // const [role, setRole] = useState<LlmRoleType>(defaultRole);
    const contentRef = useRef<HTMLTextAreaElement>(null);

    function getContent(): string {
        return contentRef.current?.value ? contentRef.current?.value : "";
    }

    function handleChange(role: LlmRoleType, content:string) {
        handleUpdate(index, {
            content,
            role,
        });
    }

    return (
        <div className="mb-2">
            <div className="flex mb-3">
                <Select
                    onValueChange={(value) => {
                        const role = value as LlmRoleType;
                        const content = getContent();
                        handleChange(role, content)
                    }}
                    value={role}
                >
                    <SelectTrigger>
                        <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                        <SelectItem value={"user"}>User</SelectItem>
                        <SelectItem value={"assistant"}>Assistant</SelectItem>
                        <SelectItem value={"system"}>System</SelectItem>
                    </SelectContent>
                </Select>
                <Button
                    className="h-8 w-8 mx-1"
                    size="icon"
                    variant="secondary"
                    onClick={() => handleMove(index, -1)}
                >
                    <i className="bi bi-chevron-up"></i>
                </Button>
                <Button
                    className="h-8 w-8 me-1"
                    size="icon"
                    variant="secondary"
                    onClick={() => handleMove(index, 1)}
                >
                    <i className="bi bi-chevron-down"></i>
                </Button>
                <Button
                    className="h-8 w-8"
                    size="icon"
                    variant="destructive"
                    onClick={() => handleDelete(index)}
                >
                    <i className="bi bi-x"></i>
                </Button>
            </div>
            <TextareaAuto
                ref={contentRef}
                value={content}
                onChange={() => {
                    const content = getContent();
                    handleChange(role, content)
                }}
            />
        </div>
    );
}
