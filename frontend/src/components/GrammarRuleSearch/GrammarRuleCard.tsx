import Text, { TextType } from '../../components/Text';

import {
    GrammarRule,
    GrammarRuleComponent,
    partOfSpeechToDisplay,
} from '../../common/api';

import {
    UserGrammarRule
} from '../../common/api/uservocabulary';

// import Button from '../Button';

type GrammarRuleCardProps = {
    grammarRule: GrammarRule;
    userGrammarRuleID?: string | null;

    handleRemoveUserGrammarRule?: (id: string) => void;
    handleAddUserGrammarRule?: (u: UserGrammarRule) => void;
}

const GrammarRuleCard = (props: GrammarRuleCardProps) => {
    return (
        <div class="w-full grid grid-cols-4">
            <div class="p-6 col-span-4 md:col-span-2 flex flex-row">
            {
                props.grammarRule.grammar_rule_components.map((c: GrammarRuleComponent) => {
                    let body = null;
                    if (!!c.word) {
                        body = (
                            <div class="flex flex-col">
                                <Text type={TextType.SectionHeader}>
                                    {c.word.display}
                                </Text>
                                <Text>
                                    {`(${c.word.pronunciation})`}
                                </Text>
                            </div>
                        );
                    } else if (!!c.part_of_speech) {
                        body = (
                            <Text type={TextType.SectionHeader}>
                                {partOfSpeechToDisplay(c.part_of_speech)}
                            </Text>
                        )
                    }
                    if (!body) {
                        return null;
                    }
                    return (
                        <div key={c.id} class="flex max-w-md py-4 px-8 bg-white shadow-lg rounded-lg items-center justify-center">
                            {body}
                        </div>
                    );
                })
            }
            </div>
            <div class="flex col-span-4 md:col-span-1 items-center justify-center">
                <Text>
                    {props.grammarRule.title}
                </Text>
            </div>
            <div class="flex col-span-4 md:col-span-1 items-center justify-center">
                <Text>
                    {props.grammarRule.definition}
                </Text>
            </div>
        </div>
    );
}

export default GrammarRuleCard;
