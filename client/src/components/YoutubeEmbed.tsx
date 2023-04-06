import React from "react";
import * as url from 'url';
import "./YoutubeEmbed.css"
import { linkFormatter } from "../utils/linkFormatter";

interface YoutubeEmbedProp {
    link: string
}

function YoutubeEmbed({ link }: YoutubeEmbedProp) {
    if (link === undefined) {
        return null
    }

    let videoId: string | null = linkFormatter(link);

    if (videoId === null) {
        return <div>
            <h1>Invalid Link</h1>
        </div>
    }





    return (
        <div>
            <iframe
                className="youtube-embed"
                src={`https://www.youtube.com/embed/${videoId}`}
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
                title="Embedded youtube"
            />
        </div >);
}

export default YoutubeEmbed;

// import { URL } from 'url';

// const url = new URL('https://www.youtube.com/watch?v=aucqOA6kyiU');
// const searchParams = url.searchParams;
// const videoId = searchParams.get('v');
