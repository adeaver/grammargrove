import { useState, useEffect } from 'preact/hooks';

import { PaginatedResponse } from '../../util/gfetch';

import Header from '../../components/Header';
import Text, { TextFunction } from '../../components/Text';
import LoadingIcon from '../../components/LoadingIcon';
import Link, { LinkTarget } from '../../components/Link';
import Button from '../../components/Button';

import {
    PracticeSession,
    createPracticeSession,
    getPracticeSession,
} from '../../common/api/practicesession';
import {
    getNextQuestion,
    Question,
} from './api';
import {
    checkPulseForm,
    FeedbackResponse,
    FeedbackType,
} from '../../components/FeedbackForm/api';
import FeedbackForm from '../../components/FeedbackForm';

import QuestionDisplay from './components/QuestionDisplay';

const PULSE_QUESTION_LIMIT = 5;
const SESSION_PARAM = "s";

const QuizPage = () => {
    const [ isLoading, setIsLoading ] = useState<boolean>(true);
    const [ question, setQuestion ] = useState<Question | null>(null);
    const [ error, setError ] = useState<Error | null>(null);
    const [ hasNextQuestion, setHasNextQuestion ] = useState<boolean>(true);
    const [ practiceSessionID, setPracticeSessionID ] = useState<string | null>(null);
    const [ practiceSessionTermsMastered, setPracticeSessionTermsMastered ] = useState<number | null>(null);
    const [ practiceSessionTotalTerms, setPracticeSessionTotalTerms ] = useState<number | null>(null);

    const [ numberOfQuestions, setNumberOfQuestions ] = useState<number>(0);
    const [ showPulseForm, setShowPulseForm ] = useState<boolean>(false);


    const makeNextQuestionRequest = (practiceSessionIDOverride: string | null) => {
        setIsLoading(true);
        getNextQuestion(
            !!practiceSessionIDOverride ? practiceSessionIDOverride : practiceSessionID,
            (resp: PaginatedResponse<Question>) => {
                setIsLoading(false);
                if (resp.results.length) {
                    const question: Question = resp.results[0];
                    setNumberOfQuestions(numberOfQuestions + 1);
                    setQuestion(question);
                    setHasNextQuestion(true);
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

    const handleAdvanceFromPulseQuestion = () => {
        setShowPulseForm(false);
        setNumberOfQuestions(numberOfQuestions + 1);
        makeNextQuestionRequest(null);
    }

    const handleGetNextQuestion = (practiceSessionIDOverride: string | null) => {
        setIsLoading(true);
        if (numberOfQuestions === PULSE_QUESTION_LIMIT) {
            checkPulseForm(
                (resp: FeedbackResponse[]) => {
                    if (!resp.length) {
                        setShowPulseForm(true);
                        setIsLoading(false);
                    } else {
                        handleAdvanceFromPulseQuestion();
                    }
                },
                (_: Error) => {
                    handleAdvanceFromPulseQuestion();
                }
            );
        } else {
            makeNextQuestionRequest(practiceSessionIDOverride);
        }
    }

    const getNewPracticeSession = () => {
        setIsLoading(true);
        createPracticeSession(
            (resp: PracticeSession) => {
                setPracticeSessionID(resp.id)
                handleGetNextQuestion(resp.id);
                setPracticeSessionTotalTerms(resp.total_number_of_terms);
                setPracticeSessionTermsMastered(0);
                window.history.pushState({ page: "quiz" }, "Quiz", `/quiz/?${SESSION_PARAM}=${resp.id}`);
            },
            (err: Error) => {
                setIsLoading(false);
                setError(err);
            }
        );
    }

    useEffect(() => {
        setIsLoading(true);
        const urlParams = new URLSearchParams(window.location.href.split("?")[1] || "");
        const urlSessionID = urlParams.get(SESSION_PARAM);
        if (!urlSessionID) {
            getNewPracticeSession();
        } else {
            getPracticeSession(
                urlSessionID,
                (resp: PracticeSession) => {
                    setPracticeSessionID(resp.id)
                    handleGetNextQuestion(resp.id);
                    setPracticeSessionTotalTerms(resp.total_number_of_terms);
                    setPracticeSessionTermsMastered(resp.terms_mastered);
                },
                (err: Error) => {
                    setIsLoading(false);
                    setError(err);
                }
            );
        }
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
    } else if (showPulseForm) {
        body = (
            <div class="p-12 w-full flex flex-col justify-center items-center space-y-4">
                <div class="max-w-2xl">
                    <FeedbackForm
                        type={FeedbackType.Pulse}
                        onSuccess={handleAdvanceFromPulseQuestion} />
                </div>
            </div>
        );
    } else if (!hasNextQuestion && !!practiceSessionID && !!practiceSessionTotalTerms) {
        body = (
            <div class="p-12 w-full flex flex-col justify-center items-center space-y-4">
                <div class="max-w-2xl flex flex-col space-y-4">
                    <Text>
                        You mastered all the words into this session.
                    </Text>
                    <Text>
                        You can start a new one here.
                    </Text>
                    <Button onClick={getNewPracticeSession}>
                        Start a new practice session
                    </Button>
                </div>
            </div>
        )

    } else if (!hasNextQuestion && !practiceSessionID) {
        // TODO: handle this case
        body = (
            <Text>
                You need to add some words
            </Text>
        )
    } else if (!!question) {
        body = (
            <QuestionDisplay
                question={question}
                practiceSessionID={practiceSessionID}
                handleGetNextQuestion={() => handleGetNextQuestion(null)} />
        )
    }
    return (
        <div class="w-full h-screen">
            <Header />
            {
                (practiceSessionTotalTerms != null) && (practiceSessionTermsMastered != null) && (
                    <div class="py-6 w-full flex flex-col space-y-4 items-center justify-center">
                        <Text>
                            { practiceSessionTotalTerms - practiceSessionTermsMastered } { (practiceSessionTotalTerms - practiceSessionTermsMastered) == 1 ? "term" : "terms" } left to master
                        </Text>
                        <div class="w-full bg-gray-200 h-5">
                            <div class="bg-confirmation-600 h-5" style={`width: ${(practiceSessionTermsMastered/practiceSessionTotalTerms) * 100}%`}></div>
                        </div>
                    </div>
                )
            }
            { body }
            <div>
                <Text>
                    Need to add a new word or grammar rule to your list?
                </Text>
                <Link href="/dashboard/" target={LinkTarget.Self}>
                    Click here to return to the dashboard
                </Link>
            </div>
        </div>
    )
}

export default QuizPage;
