import React from "react";
import { Avatar, AvatarGroup, Card } from "@chakra-ui/react";

import "./Comments.css"

interface commentsProp {
    comments: string[];
}

function Comments({ comments }: commentsProp) {
    return <div>
        {
            comments.map((comment, index) => {
                return (
                    <Card key={index} className="comments" sx={{ margin: "20px", padding: "10px", display: "flex", flexDirection: "row" }}>
                        <AvatarGroup spacing='1rem'>
                            <Avatar bg='teal.500' />
                        </AvatarGroup>
                        <p className="comment-text">{comment}</p>
                    </Card>)
            })
        }
    </div >;
}

export default Comments;
