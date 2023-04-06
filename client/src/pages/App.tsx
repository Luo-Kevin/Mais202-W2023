import React, { useState, useEffect } from 'react'
import { Heading, } from '@chakra-ui/react'

import "./App.css"
import LinkInputComponent from '../components/LinkInputComponent';
import Statistics from '../components/Statistics';
import YoutubeEmbed from '../components/YoutubeEmbed';
import Comments from '../components/Comments';

function App() {
  const [link, setLink] = useState('');
  const [result, setResult] = useState<number>(0);
  const [comments, setComments] = useState<string[]>([]);



  return (

    <div className="main-container">
      <div className='landing-section'>
        <Heading as='h1' noOfLines={1}>
          Youtube Comment Sentimental Analysis
        </Heading>
      </div>
      <div className='input-section'>
        <LinkInputComponent setLink={setLink} setData={setResult} setComments={setComments} />
      </div>
      <div className='stats'>
        <Statistics data={result} />
      </div>
      {
        link.length > 0 && link ? (
          <div className="data">
            <div className='video'>
              <YoutubeEmbed link={link} />
            </div>
            <div className='comment'>
              <Heading as='h2' noOfLines={1}>
                Top 10 Comments
              </Heading>
              <Comments comments={comments} />
            </div>

          </div>
        )
          : ("")
      }


    </div>

  )
}

export default App;