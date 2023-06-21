import Text, { TextType, TextAlignment } from '../../../components/Text';
import GrammarRuleCard from '../../../components/GrammarRuleSearch/GrammarRuleCard';

import {
    UserGrammarRule
} from '../../../common/api/uservocabulary';

type UserGrammarRulesDisplayProps = {
    grammarRules: UserGrammarRule[];

    getNextPage?: () => void;
    getPreviousPage?: () => void;
}

const UserGrammarRulesDisplay = (props: UserGrammarRulesDisplayProps) => {
    return (
        <div>
            <Text
                type={TextType.Subtitle}
                alignment={TextAlignment.Left}>
                Grammar Rules
            </Text>
            {
                props.grammarRules.map((u: UserGrammarRule) => (
                    <GrammarRuleCard key={u.id} grammarRule={u.grammar_rule} />
                ))
            }
        </div>
    )
}

export default UserGrammarRulesDisplay;
