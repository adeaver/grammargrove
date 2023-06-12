import { SearchResult } from './api';
import Button from '../Button';

type WordCardProps = {
    word: SearchResult;
    action?: WordCardAction;
    isLoading?: boolean;
}

export type WordCardAction = {
    text: string;
    action: (s: SearchResult) => void;
}

const WordCard = (props: WordCardProps) => {
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
        </div>
    );
}

export default WordCard;
