import { Word, Definition } from '../../common/api';
import Button from '../Button';

type WordCardProps = {
    word: Word;
    action?: WordCardAction;
    isLoading?: boolean;
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
    return (
        <div>
            { props.word.display }
            ( {props.word.pronunciation} )
            {
                !!props.action && (
                    <Button onClick={() => props.action!.action(props.word)} isLoading={props.isLoading}>
                        { props.action!.text }
                    </Button>
                )
            }
            { definition }
        </div>
    );
}

export default WordCard;
