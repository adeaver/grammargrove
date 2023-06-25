import { useState, useEffect } from 'preact/hooks';

import Header from '../../components/Header';
import Text, { TextFunction } from '../../components/Text';
import LoadingIcon from '../../components/LoadingIcon';

import {
    getNextQuestion,
    Question,
    // checkAnswer,
    // CheckAnswerResponse,
} from './api';

const QuizPage = () => {
    const [ isLoading, setIsLoading ] = useState<boolean>(true);
    const [ _, setQuestion ] = useState<Question | null>(null);
    const [ error, setError ] = useState<Error | null>(null);
    // const [ answer, setAnswer ] = useState<CheckAnswerResponse | null>(null);

    useEffect(() => {
        getNextQuestion(
            (resp: Question) => {
                setIsLoading(false);
                setQuestion(resp);
            },
            (err: Error) => {
                setIsLoading(false);
                setError(err);
           }
        );
    }, []);

    let body;
    if (isLoading) {
        body = (
            <LoadingIcon />
        );
    } else if (!!error) {
        body = (
            <Text function={TextFunction.Warning}>
                Something went wrong, try again later.
            </Text>
        )
    }
    return (
        <div class="w-full h-screen">
            <Header />
            { body }
        </div>
    )
}

export default QuizPage;
