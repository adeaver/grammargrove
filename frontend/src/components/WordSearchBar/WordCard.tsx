import { useState } from 'preact/hooks';

import { Word, Definition } from '../../common/api';
import Button, { ButtonType } from '../Button';
import Text, { TextType, TextAlignment } from '../Text';

import {
    UserVocabulary,

    addUserVocabulary,
    deleteUserVocabulary,
} from '../../common/api/uservocabulary';


type WordCardProps = {
    word: Word;

    userVocabularyID?: string;
    handleAddUserVocabulary?: (userVocabulary: UserVocabulary) => void;
    handleRemoveUserVocabulary?: (userVocabularyID: string) => void;
}

export type WordCardAction = {
    text: string;
    action: (s: Word) => void;
}

const WordCard = (props: WordCardProps) => {
    const definition = props.word.definitions
        .map((d: Definition) => d.definition.trim())
        .filter((d: string) => !!d)
        .join("; ");

    const [ userVocabularyID, setUserVocabularyID ] = useState<string | undefined>(props.userVocabularyID);
    const [ isLoading, setIsLoading ] = useState<boolean>(false);
    const [ error, setError ] = useState<Error | null>(null);

    let action = null;
    if (!!error) {
        action = (
            <p>Something went wrong</p>
        );
    } else if (!!userVocabularyID && !!props.handleRemoveUserVocabulary) {
        const handleRemoveFromUserVocabulary = () => {
            setIsLoading(true);
            deleteUserVocabulary(
                userVocabularyID!,
                () => {
                    setIsLoading(false);
                    props.handleRemoveUserVocabulary!(props.userVocabularyID!)
                },
                (err: Error) => {
                    setIsLoading(false);
                    setError(err);
                }
            );
        }
        action = (
            <Button type={ButtonType.Warning} onClick={handleRemoveFromUserVocabulary} isLoading={isLoading}>
                Remove from your list
            </Button>
        )
    } else if (!userVocabularyID && props.handleAddUserVocabulary) {
        const handleAddUserVocabulary = () => {
            setIsLoading(true);
            addUserVocabulary(props.word.id, null,
                (resp: UserVocabulary) => {
                    setIsLoading(false);
                    props.handleAddUserVocabulary!(resp);
                    setUserVocabularyID(resp.id);
                },
                (err: Error) => {
                    setIsLoading(false);
                    setError(err);
                }
            );
        }
        action = (
            <Button type={ButtonType.Confirmation} onClick={handleAddUserVocabulary} isLoading={isLoading}>
                Add to your list
            </Button>
        )
    }
    return (
        <div class="p-6 grid grid-cols-3">
            <div class="md:col-span-1 col-span-3 flex flex-col">
                <Text type={TextType.Title}>
                    { props.word.display }
                </Text>
                <Text>
                    {`(${props.word.pronunciation})`}
                </Text>
            </div>
            <div class="md:col-span-1 col-span-3 flex flex-col">
                <Text alignment={TextAlignment.Left}>
                    { definition }
                </Text>
            </div>
            <div class="md:col-span-1 col-span-3">
                { action }
            </div>
        </div>
    );
}

export default WordCard;
