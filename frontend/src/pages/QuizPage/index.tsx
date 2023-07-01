import { useState, useEffect } from 'preact/hooks';

import { PaginatedResponse } from '../../util/gfetch';

import Header from '../../components/Header';
import Text, { TextFunction } from '../../components/Text';
import LoadingIcon from '../../components/LoadingIcon';

import {
    getNextQuestion,
    Question,
} from './api';

import QuestionDisplay from './components/QuestionDisplay';

const QuizPage = () => {
    const [ isLoading, setIsLoading ] = useState<boolean>(true);
    const [ question, setQuestion ] = useState<Question | null>(null);
    const [ error, setError ] = useState<Error | null>(null);
    const [ hasNextQuestion, setHasNextQuestion ] = useState<boolean>(true);

    const handleGetNextQuestion = () => {
        setIsLoading(true);
        getNextQuestion(
            (resp: PaginatedResponse<Question>) => {
                setIsLoading(false);
                if (resp.results.length) {
                    const question: Question = resp.results[0];
                    // TODO: respond that we’ve seen the question
                    setQuestion(question);
                } else {
                    setHasNextQuestion(false);
                }
            },
            (err: Error) => {
                setIsLoading(false);
                setError(err);
           }
        );
    }

    useEffect(() => {
        handleGetNextQuestion();
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
    } else if (!hasNextQuestion) {
        // TODO: handle this case
        body = (
            <Text>
                You’re all out of questions.
            </Text>
        )
    } else if (!!question) {
        body = (
            <QuestionDisplay
                question={question}
                handleGetNextQuestion={handleGetNextQuestion} />
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
