import { useState } from 'preact/hooks';

import Text, { TextType, TextAlignment, TextFunction } from '../../../components/Text';

import { Word } from '../../../common/api';
import WordSearchBar from '../../../components/WordSearchBar';
import WordCard from '../../../components/WordSearchBar/WordCard';

import {
    UserVocabulary
} from '../../../common/api/uservocabulary';

type UserVocabularyDisplayProps = {
    vocabulary: UserVocabulary[];
    removeFromUserVocabulary: (id: string) => void;
    handleAddUserVocabulary: (u: UserVocabulary) => void;

    getNextPage?: () => void;
    getPreviousPage?: () => void;
}

const UserVocabularyDisplay = (props: UserVocabularyDisplayProps) => {
    const [ wordSearchResults, setWordSearchResults ] = useState<Word[] | undefined>(undefined);
    const [ wordSearchError, setWordSearchError ] = useState<Error | null>(null);

    return (
        <div>
            <Text
                type={TextType.Subtitle}
                alignment={TextAlignment.Left}>
                Vocabulary Words
            </Text>
            {
                props.vocabulary.map((u: UserVocabulary) => (
                    <WordCard
                        key={u.id}
                        word={u.word}
                        userVocabularyID={u.id}
                        handleRemoveUserVocabulary={props.removeFromUserVocabulary} />
                ))
            }
            <Text>
                Search for a new word
            </Text>
            <WordSearchBar
                onSuccess={setWordSearchResults}
                onError={setWordSearchError} />
            <WordSearchBody
                error={wordSearchError}
                results={wordSearchResults}
                handleAddUserVocabulary={props.handleAddUserVocabulary}
                handleRemoveUserVocabulary={props.removeFromUserVocabulary} />
        </div>
    )
}

type WordSearchBodyProps = {
    error: Error | null;
    results: Word[] | undefined;

    handleAddUserVocabulary: (u: UserVocabulary) => void;
    handleRemoveUserVocabulary: (id: string) => void;
}

const WordSearchBody = (props: WordSearchBodyProps) => {
    if (!!props.error) {
        return (
            <Text function={TextFunction.Warning}>
                There was an error searching.
            </Text>
        );
    } else if (!props.results && props.results === undefined) {
        return (
            <Text function={TextFunction.Warning}>
                No results
            </Text>
        )
    }
    return (
        <div>
        {
            props.results!.map((w: Word) => {
                return (
                    <WordCard
                        key={w.id}
                        word={w}
                        handleAddUserVocabulary={props.handleAddUserVocabulary}
                        handleRemoveUserVocabulary={props.handleRemoveUserVocabulary} />
                )
            })
        }
        </div>
    )
}

export default UserVocabularyDisplay;
