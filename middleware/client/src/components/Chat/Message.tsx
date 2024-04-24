import { Button } from "../../@shadcn/components/ui/button";
import { Card, CardContent, CardFooter, CardHeader } from "../../@shadcn/components/ui/card";

function EditingMessage(){
    return (
        <div>
            
        </div>
    );
}

export default function Message() {
    return (
        <Card className="w-full relative">
            <div className="pe-10">
            <CardHeader className="py-2 px-3">
                <span>User</span>
            </CardHeader>
            <CardContent className="py-2 px-3">
                the content
            </CardContent>
            </div>
            <Button className="absolute bottom-0 right-0 m-1 size-8" variant="secondary"><i className="bi bi-pencil-fill"></i></Button>
        </Card>
    );
}
