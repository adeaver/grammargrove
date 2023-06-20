import { useState } from 'preact/hooks';

import WordSearchBar from '../../../components/WordSearchBar';
import { SearchResult } from '../../../components/WordSearchBar/api';
import WordCard from '../../../components/WordSearchBar/WordCard';

import {
    UserVocabulary,
    addUserVocabulary,
    deleteUserVocabulary,
} from '../api';

export type WordSearchProps = {
    userVocabularyByWordID: { [key: string]: UserVocabulary };
    loadingWords: { [key: string]: boolean };

    setLoadingWords: (loadingWords: { [key: string]: boolean }) => void;
    setUserVocabularyByWordID: (userVocabularyByWordID: { [key: string]: UserVocabulary }) => void;

    setError: (err: Error | null) => void;
}

const WordSearch = (props: WordSearchProps) => {
    const [ searchResults, setSearchResults ] = useState<SearchResult[]>([]);

    const handleLoadingWord = (wordID: string, isLoading: boolean) => {
        if (isLoading) {
            props.setLoadingWords({
                ...props.loadingWords,
                [wordID]: true,
            });
        } else {
            props.setLoadingWords(
                Object.keys(props.loadingWords).reduce(
                    (acc: { [key: string]: boolean }, curr: string) => {
                        if (curr == wordID) {
                            return acc
                    }
                    return {
                        ...acc,
                        [wordID]: true,
                    }
                }, {})
            );
        }
    }


    const handleAddWordToVocabulary = (wordID: string) => {
        handleLoadingWord(wordID, true);
        addUserVocabulary(
            wordID, null,
            (resp: UserVocabulary) => {
                handleLoadingWord(wordID, false);
                props.setUserVocabularyByWordID({
                    ...props.userVocabularyByWordID,
                    [ resp.word.id ]: resp,
                });
                props.setError(null);
            },
            (err: Error) => {
                handleLoadingWord(wordID, false);
                props.setError(err);
            }
        );
    }

    const handleDeleteVocabularyEntry = (wordID: string) => {
        handleLoadingWord(wordID, true);
        const id: string | null = props.userVocabularyByWordID[wordID].id || null;
        if (!id) {
            handleLoadingWord(wordID, false);
            return;
        }
        deleteUserVocabulary(
            id,
            () => {
                handleLoadingWord(wordID, false);
                props.setUserVocabularyByWordID(
                    Object.values(props.userVocabularyByWordID).reduce(
                        (acc: { [key: string]: UserVocabulary }, curr: UserVocabulary) => {
                            if (curr.id === id) {
                                return acc
                            }
                            return {
                                ...acc,
                                [curr.word.id]: curr,
                            }
                        }, {}
                    )
                );
                props.setError(null);
            },
            (err: Error) => {
                handleLoadingWord(wordID, false);
                props.setError(err);
            }
        );
    }

    return (
        <div>
            <WordSearchBar
                onSuccess={setSearchResults} />
            {
                searchResults.map((s: SearchResult) => {
                    const action = !!props.userVocabularyByWordID[s.word_id] ? ({
                            text: 'Remove from Vocabulary',
                            action: (s: SearchResult) => { handleDeleteVocabularyEntry(s.word_id) },
                        }) : ({
                            text: 'Add to Vocabulary',
                            action: (s: SearchResult) => { handleAddWordToVocabulary(s.word_id) },
                        });
                    return (
                        <WordCard
                            key={s.word_id}
                            isLoading={props.loadingWords[s.word_id]}
                            word={s}
                            action={action} />
                    );
                })
            }
        </div>
    )
}

export default WordSearch;
