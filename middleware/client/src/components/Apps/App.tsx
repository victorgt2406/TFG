import { toast } from "sonner";
import { Button } from "../../@shadcn/components/ui/button";
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from "../../@shadcn/components/ui/card";
import type { AppModel } from "../../models/App";
import AppContent from "./AppContent";
import type { LlmMessageType } from "../../models/LlmMessage";
import { useState } from "react";

export default function App({
    name,
    description,
    terms: defaultTerms,
    conclusions: defaultConclusions,
}: Required<AppModel>) {
    const [terms, setTerms] = useState(defaultTerms);
    const [conclusions, setConclusions] = useState(defaultConclusions);

    async function handleUpdate(
        array: LlmMessageType[],
        setArray: (array: LlmMessageType[]) => void,
        index: number,
        newContent?: LlmMessageType
    ) {
        if (array && index >= 0 && index < array.length) {
            const arrayCopy = [...array];
            if (newContent) {
                arrayCopy[index] = newContent;
                toast("content updated");
            }
            else {
                arrayCopy.splice(index);
                toast("content deleted");
            }
            setArray(arrayCopy);
        } 
        else if (index === -1 && newContent){
            setArray([...array, newContent])
            toast("Empty message created");
        }
        else toast("error");
    }

    const handleUpdateTerms = async (
        index: number,
        newContent?: LlmMessageType
    ) => await handleUpdate(terms, setTerms, index, newContent);

    const handleUpdateConclusions = async (
        index: number,
        newContent?: LlmMessageType
    ) => await handleUpdate(conclusions, setConclusions, index, newContent);

    return (
        <Card className="relative mt-2">
            <CardHeader>
                <CardTitle>{name}</CardTitle>
                <CardDescription>{description}</CardDescription>
            </CardHeader>
            <CardContent>
                <AppContent
                    conclusions={conclusions}
                    terms={terms}
                    handleUpdateTerms={handleUpdateTerms}
                    handleUpdateConclusions={handleUpdateConclusions}
                />
            </CardContent>
            <Button
                className="absolute top-0 right-0 m-2 h-8 w-8"
                size="icon"
                variant="destructive"
            >
                <i className="bi bi-x"></i>
            </Button>
        </Card>
    );
}
