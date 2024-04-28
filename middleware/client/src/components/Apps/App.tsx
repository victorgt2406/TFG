import {
    Accordion,
    AccordionContent,
    AccordionItem,
    AccordionTrigger,
} from "../../@shadcn/components/ui/accordion";
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

export default function App({
    name,
    description,
    terms,
    conclusions,
}: Required<AppModel>) {
    return (
        <Card className="relative mt-2">
            <CardHeader className="pr-20">
                <CardTitle>{name}</CardTitle>
                <CardDescription>{description}</CardDescription>
            </CardHeader>
            <CardContent>
                <Accordion type="single" collapsible className="w-full">
                    <AccordionItem value="terms">
                        <AccordionTrigger>Terms</AccordionTrigger>
                        <AppContent
                            messages={terms.map((value, index) => {
                                return { ...value, index };
                            })}
                        />
                    </AccordionItem>
                    <AccordionItem value="conclusion">
                        <AccordionTrigger>Conclusion</AccordionTrigger>
                        <AppContent
                            messages={conclusions.map((value, index) => {
                                return { ...value, index };
                            })}
                        />
                    </AccordionItem>
                </Accordion>
                {/* <AppContent conclusions={conclusions} terms={terms} /> */}
            </CardContent>
            <div className="absolute top-0 right-0 m-2">
                <Button className="h-8 w-8 me-1" size="icon">
                    <i className="bi bi-floppy"></i>
                </Button>
                <Button className="h-8 w-8" size="icon" variant="destructive">
                    <i className="bi bi-trash3"></i>
                </Button>
            </div>
        </Card>
    );
}
