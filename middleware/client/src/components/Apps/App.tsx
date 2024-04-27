import { Button } from "../../@shadcn/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../../@shadcn/components/ui/card";
import type { AppModel } from "../../models/App";

export default function ({name, description, terms, conclusions}:AppModel) {
    return (
        <Card className="relative pr-12">
            <CardHeader>
                <CardTitle>{name}</CardTitle>
                <CardDescription>{description}</CardDescription>
            </CardHeader>
            <CardContent>
                {/* <span>{terms}</span>
                <span>{conclusions}</span> */}
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
