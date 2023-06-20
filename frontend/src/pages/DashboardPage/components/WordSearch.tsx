import { useState } from 'preact/hooks';

import WordSearchBar from '../../../components/WordSearchBar';
import { Word } from '../../../common/api';
import WordCard from '../../../components/WordSearchBar/WordCard';

import {
    UserVocabulary,
    addUserVocabulary,
    deleteUserVocabulary,
} from '../../../common/api/uservocabulary';

export type WordSearchProps = {
    userVocabularyByWordID: { [key: string]: UserVocabulary };
    loadingWords: { [key: string]: boolean };

    setLoadingWords: (loadingWords: { [key: string]: boolean }) => void;
    setUserVocabularyByWordID: (userVocabularyByWordID: { [key: string]: UserVocabulary }) => void;

    setError: (err: Error | null) => void;
}

const WordSearch = (props: WordSearchProps) => {
    const [ searchResults, setSearchResults ] = useState<Word[]>([]);

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
                searchResults.map((s: Word) => {
                    const action = !!props.userVocabularyByWordID[s.id] ? ({
                            text: 'Remove from Vocabulary',
                            action: (s: Word) => { handleDeleteVocabularyEntry(s.id) },
                        }) : ({
                            text: 'Add to Vocabulary',
                            action: (s: Word) => { handleAddWordToVocabulary(s.id) },
                        });
                    return (
                        <WordCard
                            key={s.id}
                            isLoading={props.loadingWords[s.id]}
                            word={s}
                            action={action} />
                    );
                })
            }
        </div>
    )
}

export default WordSearch;
