import axios from "axios";
import { useState } from "react";
const environment = import.meta.env.MDW_HOST;



export default function(){
    // State for the input field
    const [inputText, setInputText] = useState("");
    // State for the textarea
    const [textAreaContent, setTextAreaContent] = useState("");

    // Function to handle the input change
    const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setInputText(event.target.value);
    };

    // Function to handle the textarea change
    const handleTextAreaChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
        setTextAreaContent(event.target.value);
    };

    // Function to handle the button click
    const handleButtonClick = async () => {
        const response = await axios.post("http://localhost:2002/api/chat/",{
            message: inputText
        })
        console.log(response)
        setTextAreaContent(response.data.conclusion)
    };

    return (
        <div>
            <input
                type="text"
                value={inputText}
                onChange={handleInputChange}
                placeholder="Message"
            />
            <button onClick={handleButtonClick}>Click Me</button>
            <textarea
                value={textAreaContent}
                onChange={handleTextAreaChange}
                placeholder=""
                disabled
            />
        </div>
    );
}