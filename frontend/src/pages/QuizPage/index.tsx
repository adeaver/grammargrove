import { useEffect, useState } from 'preact/hooks';

import QuestionDisplay from './components/QuestionDisplay';
import {
    getNextQuestion,
    Question
} from './api';

const QuizPage = () => {
    const [ isLoading, setIsLoading ] = useState<boolean>(true);
    const [ question, setQuestion ] = useState<Question | null>(null);
    const [ error, setError ] = useState<Error | null>(null);

    useEffect(() => {
        getNextQuestion(
            (q: Question) => {
                setIsLoading(false);
                setQuestion(q);
                setError(null);
            },
            (err: Error) => {
                setIsLoading(false);
                setError(err);
            }
        );
    }, []);

    if (isLoading) {
        return <p>Loading</p>
    } else if (!question) {
        return <p>There has been an error</p>
    }
    return (
        <div>
            {
                !!error && (
                    <p>There has been an error</p>
                )
            }
            <QuestionDisplay question={question} />
        </div>
    );
}

export default QuizPage;
