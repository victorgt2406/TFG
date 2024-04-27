import React from "react";
import {
    Accordion,
    AccordionContent,
    AccordionItem,
    AccordionTrigger,
} from "../../@shadcn/components/ui/accordion";
import type { AppModel } from "../../models/App";
import ContextMessage from "./ContextMessage";
import type { LsmMessageType } from "../../models/LsmMessage";
import { toast } from "sonner";
import type { LlmMessageType } from "../../models/LlmMessage";
import type { LlmRoleType } from "../../models/LlmRole";
import { Button } from "../../@shadcn/components/ui/button";

type handleUpdateType = (
    index: number,
    newContent?: LlmMessageType
) => Promise<void>;

type MyProps = Required<Pick<AppModel, "conclusions" | "terms">> & {
    handleUpdateTerms: handleUpdateType;
    handleUpdateConclusions: handleUpdateType;
};

export default function MessageFooter({
    terms,
    conclusions,
    handleUpdateConclusions,
    handleUpdateTerms,
}: MyProps) {
    function handleCreateContextMessage(handleUpdate: handleUpdateType) {
        handleUpdate(-1, {
            role: "user",
            content: "",
        });
    }

    return (
        <Accordion type="single" collapsible className="w-full">
            <AccordionItem value="terms">
                <AccordionTrigger>Terms</AccordionTrigger>
                <AccordionContent className="p-2">
                    {terms.map((term, index) => (
                        <ContextMessage
                            key={index}
                            {...term}
                            handleUpdateContent={async (content) =>
                                await handleUpdateTerms(index, content)
                            }
                        />
                    ))}
                    <Button
                        onClick={() =>
                            handleCreateContextMessage(handleUpdateTerms)
                        }
                    >
                        Create Context Message
                    </Button>
                </AccordionContent>
            </AccordionItem>
            <AccordionItem value="conclusion">
                <AccordionTrigger>Conclusion</AccordionTrigger>
                <AccordionContent>
                    {conclusions.map((term, index) => (
                        <ContextMessage
                            key={index}
                            {...term}
                            handleUpdateContent={async (content) =>
                                await handleUpdateConclusions(index, content)
                            }
                        />
                    ))}
                    <Button
                        onClick={() =>
                            handleCreateContextMessage(handleUpdateConclusions)
                        }
                    >
                        Create Context Message
                    </Button>
                </AccordionContent>
            </AccordionItem>
        </Accordion>
    );
}
