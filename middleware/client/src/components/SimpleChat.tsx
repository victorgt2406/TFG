import axios from "axios";
import { useState } from "react";
const environment = import.meta.env.MDW_HOST;

export default function () {
    // State for the input field
    const [inputText, setInputText] = useState("");
    // State for the textarea
    const [textAreaContent, setTextAreaContent] = useState("");

    // Function to handle the input change
    const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setInputText(event.target.value);
    };

    // Function to handle the textarea change
    const handleTextAreaChange = (
        event: React.ChangeEvent<HTMLTextAreaElement>
    ) => {
        setTextAreaContent(event.target.value);
    };

    // Function to handle the button click
    const handleButtonClick = async () => {
        const response = await axios.post("http://localhost:3000/api/chat/", {
            message: inputText,
        });
        console.log(response);
        setTextAreaContent(response.data.conclusion);
    };

    return (
        <div className="flex flex-col my-3">
            <textarea
                value={textAreaContent}
                onChange={handleTextAreaChange}
                placeholder=""
                disabled
                className="h-64"
            />
            <hr className="my-2" />
            <div className="flex">
                <input
                    type="text"
                    value={inputText}
                    onChange={handleInputChange}
                    placeholder="Message"
                    className="w-10/12"
                />
                <button
                    className="bg-blue-500 text-white px-4 py-2 border border-blue-500 rounded hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-300 focus:ring-opacity-50 transition duration-150 w-2/12"
                    onClick={handleButtonClick}
                >
                    chat!
                </button>
            </div>
        </div>
    );
}
