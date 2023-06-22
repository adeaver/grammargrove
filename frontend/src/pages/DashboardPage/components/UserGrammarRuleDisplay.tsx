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
        <div class="p-6">
            <div class="flex flex-col md:flex-row justify-between items-center">
                <div>
                    <Text
                        type={TextType.Subtitle}
                        alignment={TextAlignment.Left}>
                        Grammar Rules
                    </Text>
                </div>
            </div>
            <hr class="my-4 border-2 border-slate-600" />
            {
                props.grammarRules.map((u: UserGrammarRule) => (
                    <GrammarRuleCard key={u.id} grammarRule={u.grammar_rule} />
                ))
            }
        </div>
    )
}

export default UserGrammarRulesDisplay;
