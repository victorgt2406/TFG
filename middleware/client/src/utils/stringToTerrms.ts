export default function stringToTerms(text: string){
    return text.replace(" ", "").split(",")
}