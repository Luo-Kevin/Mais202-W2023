import React from "react";
import { CircularProgress, Card, Heading, CircularProgressLabel } from '@chakra-ui/react'
import "./Statistics.css"

interface StatisticsProps {
    data: number;
}

function Statistics({ data }: StatisticsProps) {
    let result: number;
    result = data * 100;

    // if (result <= 70 && result > 50) {
    //     result /= 1.5;
    // } else if (result <= 50) {
    //     result /= 2;
    // }


    let color: string = '';

    if (result >= 75) {
        color = 'green.400'
    } else if (result < 75 && result >= 50) {
        color = 'yellow.400'
    } else if (result < 50) {
        color = 'red.400'
    }

    result = Math.round(result);

    // console.log(result)
    return (
        <div className="stats">
            <Card className="result">
                <Heading size='xs' textTransform='uppercase'>
                    Sentiment Score
                </Heading>
                {data === -1 ? (
                    <div>
                        <CircularProgress isIndeterminate color='green.300' />
                    </div>
                ) : (
                    <div className="circular-bar">
                        <CircularProgress value={result} color={color}>
                        </CircularProgress>
                        <CircularProgressLabel>{result <= 0 ? '--' : `${result}`}%</CircularProgressLabel>
                    </div>
                )}
            </Card>

        </div >
    );
}

export default Statistics;
