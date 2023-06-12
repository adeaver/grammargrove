import { useEffect, useState } from 'preact/hooks';

import WordSearchBar from '../../components/WordSearchBar';
import { SearchResult } from '../../components/WordSearchBar/api';
import WordCard from '../../components/WordSearchBar/WordCard';

import {
    UserVocabulary,
    getUserVocabulary,
    addUserVocabulary,
    deleteUserVocabulary,
} from './api';

const Dashboard = () => {
    const [ isLoading, setIsLoading ] = useState<boolean>(true);

    const [ searchResults, setSearchResults ] = useState<SearchResult[]>([]);
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

    const handleAddWordToVocabulary = (s: SearchResult) => {
        setIsLoading(true);
        addUserVocabulary(
            s.word_id, null,
            (resp: UserVocabulary) => {
                setIsLoading(false);
                setUserVocabularyByWordID({
                    ...userVocabularyByWordID,
                    [ resp.word ]: resp,
                });
                setError(null);
            },
            (err: Error) => {
                setIsLoading(false);
                setError(err);
            }
        );
    }

    const handleDeleteVocabularyEntry = (s: SearchResult) => {
        setIsLoading(true);
        const id: string | null = userVocabularyByWordID[s.word_id].id || null;
        if (!id) {
            setIsLoading(false);
            return;
        }
        deleteUserVocabulary(
            id,
            () => {
                setIsLoading(false);
                setUserVocabularyByWordID(
                    Object.values(userVocabularyByWordID).reduce(
                        (acc: { [key: string]: UserVocabulary }, curr: UserVocabulary) => {
                            if (curr.id === id) {
                                return acc
                            }
                            return {
                                ...acc,
                                [curr.word]: curr,
                            }
                        }, {}
                    )
                );
                setError(null);
            },
            (err: Error) => {
                setIsLoading(false);
                setError(err);
            }
        );
    }

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
            <WordSearchBar
                onSuccess={setSearchResults} />
            {
                searchResults.map((s: SearchResult) => {
                    const action = !!userVocabularyByWordID[s.word_id] ? ({
                            text: 'Remove from Vocabulary',
                            action: handleDeleteVocabularyEntry,
                        }) : ({
                            text: 'Add to Vocabulary',
                            action: handleAddWordToVocabulary,
                        });
                    return (
                        <WordCard
                            key={s.word_id}
                            word={s}
                            action={action} />
                    );
                })
            }
        </div>
    )
}

export default Dashboard;
