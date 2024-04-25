import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "../../@shadcn/components/ui/accordion";
import type { LsmResponseType } from "../../models/LsmResponse";

export default function MessageFooter({terms, docs}:LsmResponseType) {
    return (
        <Accordion type="single" collapsible className="w-full">
            <AccordionItem value="terms">
                <AccordionTrigger>Terms</AccordionTrigger>
                <AccordionContent>
                    {terms}
                </AccordionContent>
            </AccordionItem>
            <AccordionItem value="docs">
                <AccordionTrigger>Docs</AccordionTrigger>
                <AccordionContent>
                    <pre>{JSON.stringify(docs,undefined,2)}</pre>
                </AccordionContent>
            </AccordionItem>
        </Accordion>
    );
}
