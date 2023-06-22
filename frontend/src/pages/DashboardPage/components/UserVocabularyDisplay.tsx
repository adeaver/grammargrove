import { useState } from 'preact/hooks';

import Text, { TextType, TextAlignment, TextFunction } from '../../../components/Text';
import Button, { ButtonType } from '../../../components/Button';

import { Word } from '../../../common/api';
import WordSearchBar from '../../../components/WordSearchBar';
import WordCard from '../../../components/WordSearchBar/WordCard';

import {
    UserVocabulary
} from '../../../common/api/uservocabulary';

type UserVocabularyDisplayProps = {
    isLoading: boolean;
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
        <div class="p-6">
            <div class="flex flex-col md:flex-row justify-between items-center">
                <div>
                    <Text
                        type={TextType.Subtitle}
                        alignment={TextAlignment.Left}>
                        Vocabulary Words
                    </Text>
                </div>
                <PageNavigationButtons
                    getNextPage={props.getNextPage}
                    getPreviousPage={props.getPreviousPage} />
            </div>
            <hr class="my-4 border-2 border-slate-600" />
            {
                props.isLoading ? (
                    "Loading..."
                ) : (
                    <div>
                        {
                            props.vocabulary.map((u: UserVocabulary) => (
                                <WordCard
                                    key={u.id}
                                    word={u.word}
                                    userVocabularyID={u.id}
                                    handleRemoveUserVocabulary={props.removeFromUserVocabulary} />
                            ))
                        }
                        <Text alignment={TextAlignment.Left} type={TextType.SectionHeader}>
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
    } else if (!props.results && props.results != undefined) {
        return (
            <Text function={TextFunction.Warning}>
                No results
            </Text>
        )
    }
    return (
        <div>
        {
            (props.results || []).map((w: Word) => {
                return (
                    <WordCard
                        key={w.id}
                        word={w}
                        handleAddUserVocabulary={props.handleAddUserVocabulary}
                        handleRemoveUserVocabulary={props.handleRemoveUserVocabulary}
                        userVocabularyID={w.user_vocabulary_entry} />
                )
            })
        }
        </div>
    )
}

type PageNavigationButtonsProps = {
    getNextPage?: () => void;
    getPreviousPage?: () => void;
}

const PageNavigationButtons = (props: PageNavigationButtonsProps) => {
    return (
        <div class="flex flex-row space-x-4">
            {
                !!props.getPreviousPage && (
                    <Button type={ButtonType.Secondary} onClick={props.getPreviousPage}>
                        Previous Page
                    </Button>
                )
            }
            {
                !!props.getNextPage && (
                    <Button type={ButtonType.Secondary} onClick={props.getNextPage}>
                        Next Page
                    </Button>
                )
            }
        </div>
    )
}

export default UserVocabularyDisplay;
