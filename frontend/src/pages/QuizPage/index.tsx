import { useEffect, useState } from 'preact/hooks';

import Button from '../../components/Button';

import QuestionDisplay from './components/QuestionDisplay';
import {
    getNextQuestion,
    Question,
    checkAnswer,
    CheckAnswerResponse,
} from './api';

const QuizPage = () => {
    const [ isLoading, setIsLoading ] = useState<boolean>(true);
    const [ question, setQuestion ] = useState<Question | null>(null);
    const [ error, setError ] = useState<Error | null>(null);

    const [ answer, setAnswer ] = useState<CheckAnswerResponse | null>(null);

    const handleSubmitAnswer = (a: string) => {
        setIsLoading(true);
        if (!question) {
            setIsLoading(false);
            return;
        }
        checkAnswer(
            question.question_id, a,
            (resp: CheckAnswerResponse) => {
                setIsLoading(false);
                setAnswer(resp);
                setError(null);
            },
            (err: Error) => {
                setIsLoading(false);
                setAnswer(null);
                setError(err);
            }
        );
    }

    const handleGetNextQuestion = () => {
        setIsLoading(true);
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
    }

    useEffect(() => {
        handleGetNextQuestion();
    }, []);

    // TODO: display answer more nicely
    let answerText: string | null = null;
    if (!!answer && answer.correct) {
        answerText = "That's correct!"
    } else if (!!answer && !answer.correct) {
        answerText = `That's not correct. The correct answer is ${answer.correct_answer}`
    }

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
            {
                !!answerText && (
                    <p>{answerText}</p>
                )
            }
            <QuestionDisplay
                question={question}
                isLoading={isLoading}
                submitAnswer={handleSubmitAnswer} />
            {
                !!answerText && (
                    <Button onClick={handleGetNextQuestion} isLoading={isLoading}>
                        Next Question
                    </Button>
                )
            }
        </div>
    );
}

export default QuizPage;
