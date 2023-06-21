import Text, { TextType, TextAlignment } from '../../../components/Text';
import WordCard from '../../../components/WordSearchBar/WordCard';

import {
    UserVocabulary
} from '../../../common/api/uservocabulary';

type UserVocabularyDisplayProps = {
    vocabulary: UserVocabulary[];

    getNextPage?: () => void;
    getPreviousPage?: () => void;
}

const UserVocabularyDisplay = (props: UserVocabularyDisplayProps) => {
    return (
        <div>
            <Text
                type={TextType.Subtitle}
                alignment={TextAlignment.Left}>
                Vocabulary Words
            </Text>
            {
                props.vocabulary.map((u: UserVocabulary) => (
                    <WordCard key={u.id} word={u.word} />
                ))
            }
        </div>
    )
}

export default UserVocabularyDisplay;
