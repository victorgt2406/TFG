export default function createConclusionQuery(message:string, documents:any[]){
    return `**Docs**: ${JSON.stringify(documents,null, 4)}\n**User Message**: "${message}"`
}