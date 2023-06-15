import { useEffect, useState } from 'preact/hooks';

import {
    UserVocabulary,
    getUserVocabulary,
} from './api';

import WordSearch from './components/WordSearch';
import GrammarSearch from './components/GrammarSearch';

const Dashboard = () => {
    const [ isLoading, setIsLoading ] = useState<boolean>(true);
    const [ loadingWords, setLoadingWords ] = useState<{ [key: string]: boolean }>({});
    const [ userVocabularyByWordID, setUserVocabularyByWordID ] = useState<{ [word_id: string]: UserVocabulary }>({});
    const [ error, setError ] = useState<Error | null>(null);

    useEffect(() => {
        getUserVocabulary(
            (resp: UserVocabulary[]) => {
                setIsLoading(false);
                setError(null);
                setUserVocabularyByWordID(
                    resp.reduce((acc: { [word: string]: UserVocabulary }, curr: UserVocabulary) => ({
                        ...acc,
                        [curr.word]: curr,
                    }), {})
                );
            },
            (err: Error) => {
                setIsLoading(false);
                setError(err);
            }
        );
    }, []);


    if (isLoading) {
        // Entire page is loading
        return (
            <div>
                Loading ...
            </div>
        )
    } else if (!!error) {
        return (
            <div>
                An error occurred. Try again later.
            </div>
        )
    }
    return (
        <div>
            <WordSearch
                userVocabularyByWordID={userVocabularyByWordID}
                loadingWords={loadingWords}
                setUserVocabularyByWordID={setUserVocabularyByWordID}
                setLoadingWords={setLoadingWords}
                setError={setError} />
            <GrammarSearch />
        </div>
    )
}

export default Dashboard;
