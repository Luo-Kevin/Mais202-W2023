import React, { useState } from "react";
import {
    Button,
    FormControl,
} from '@chakra-ui/react'
import { Input } from '@chakra-ui/react'

import "./LinkInputComponent.css"
import bodyProps from "../models/models";
import { model } from "../utils/api"
import { linkFormatter } from "../utils/linkFormatter";
interface LinkInputProps {
    setLink: React.Dispatch<React.SetStateAction<string>>;
    setData: React.Dispatch<React.SetStateAction<number>>;
    setComments: React.Dispatch<React.SetStateAction<string[]>>;
}

function LinkInputComponent({ setLink, setData, setComments }: LinkInputProps) {
    const [temporaryLink, setTemporaryLink] = useState("");

    const handleSubmit = async (e: any) => {
        e.preventDefault();

        setData(-1)
        setComments([])
        setLink("")
        const id: string | null = linkFormatter(temporaryLink);


        if (id === null) {
            return (
                <div>
                    <h1>Invalid Link</h1>
                </div>
            );
        }

        const videoId: bodyProps = {
            link: id ?? ""
        }

        const response = await model(videoId);
        const decimalSeparator = "."; // Replace with the decimal separator used in your data
        const cleanString = response.data.replace(/[^\d.,]/g, "").replace(",", decimalSeparator);
        const result = parseFloat(cleanString);
        setLink(temporaryLink);
        setData(result);
        setComments(response.comments);
    }


    return (
        <form className="input-form">
            <FormControl isRequired>
                <Input className="link-input" placeholder='Enter a link to a YouTube video' onChange={(e) => { setTemporaryLink(e.target.value) }} />
            </FormControl>
            <Button type="submit" colorScheme='blue' onClick={handleSubmit}>
                Analyze
            </Button>
        </form>

    )
}

export default LinkInputComponent;
