import {
    GrammarRuleComponent,
    partOfSpeechToDisplay,
} from '../../common/api';

import { SearchResult } from './api';
import Button from '../Button';

type GrammarRuleCardProps = {
    grammarRule: SearchResult;
    action?: GrammarRuleCardAction;
    isLoading?: boolean;
}

export type GrammarRuleCardAction = {
    text: string;
    action: (s: SearchResult) => void;
}

const GrammarRuleCard = (props: GrammarRuleCardProps) => {
    return (
        <div>
            <p>{props.grammarRule.grammar_rule.title}</p>
            <p>{props.grammarRule.grammar_rule.definition}</p>
            {
                props.grammarRule.components.map((c: GrammarRuleComponent) => {
                    if (!!c.word) {
                        return (
                            <p key={c.id}>{c.word.display} ({c.word.pronunciation})</p>
                        );
                    } else if (!!c.part_of_speech) {
                        return (
                            <p key={c.id}>{partOfSpeechToDisplay(c.part_of_speech)}</p>
                        )
                    }
                    return null;
                })
            }
            {
                !!props.action && (
                    <Button onClick={() => props.action!.action(props.grammarRule)} isLoading={props.isLoading}>
                        { props.action!.text }
                    </Button>
                )
            }
        </div>
    );
}

export default GrammarRuleCard;
