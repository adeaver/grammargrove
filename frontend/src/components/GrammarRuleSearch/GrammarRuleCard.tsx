import { useState } from 'preact/hooks';

import Text, { TextType, TextFunction } from '../../components/Text';
import Button, { ButtonType } from '../../components/Button';

import {
    GrammarRule,
    GrammarRuleComponent,
    partOfSpeechToDisplay,
} from '../../common/api';

import {
    UserGrammarRule,

    addUserGrammarRule,
    deleteUserGrammarRule,
} from '../../common/api/uservocabulary';

type GrammarRuleCardProps = {
    grammarRule: GrammarRule;
    userGrammarRuleID?: string | null;

    handleRemoveUserGrammarRule?: (id: string) => void;
    handleAddUserGrammarRule?: (u: UserGrammarRule) => void;
}

const GrammarRuleCard = (props: GrammarRuleCardProps) => {
    const [ userGrammarRuleID, setUserGrammarRuleID ] = useState<string | null | undefined>(props.userGrammarRuleID);
    const [ isLoading, setIsLoading ] = useState<boolean>(false);
    const [ error, setError ] = useState<Error | null>(null);

    let action;
    if (!!error) {
        action = (
            <Text function={TextFunction.Warning}>
                Something went wrong. Try again later.
            </Text>
        )
    } else if (!userGrammarRuleID && !!props.handleAddUserGrammarRule) {
        const handleAddUserGrammarRule = () => {
            setIsLoading(true);
            addUserGrammarRule(
                props.grammarRule.id, null,
                (resp: UserGrammarRule) => {
                    setIsLoading(false);
                    setUserGrammarRuleID(resp.id);
                    props.handleAddUserGrammarRule!(resp);
                },
                (err: Error) => {
                    setIsLoading(false);
                    setError(err);
                }
            );
        }
        action = (
            <Button
                type={ButtonType.Confirmation}
                onClick={handleAddUserGrammarRule}
                isLoading={isLoading}>
                Add to your list
            </Button>
        )
    } else if (userGrammarRuleID && !!props.handleRemoveUserGrammarRule) {
        const handleRemoveUserGrammarRule = () => {
            setIsLoading(true);
            deleteUserGrammarRule(userGrammarRuleID,
                () => {
                    setIsLoading(false);
                    props.handleRemoveUserGrammarRule!(userGrammarRuleID);
                    setUserGrammarRuleID(null);
                },
                (err: Error) => {
                    setIsLoading(false);
                    setError(err);
                }
            );
        }
        action = (
            <Button
                type={ButtonType.Warning}
                onClick={handleRemoveUserGrammarRule}
                isLoading={isLoading}>
                Remove from your list
            </Button>
        )
    }

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
                        <div key={c.id} class="flex mx-2 py-4 px-8 bg-white shadow-lg rounded-lg items-center justify-center">
                            {body}
                        </div>
                    );
                })
            }
            </div>
            <div class="flex flex-col col-span-4 md:col-span-1 items-center justify-center">
                <Text>
                    {props.grammarRule.title}
                </Text>
                <Text type={TextType.FinePrint}>
                    {props.grammarRule.definition}
                </Text>
            </div>
            <div class="flex col-span-4 md:col-span-1 items-center justify-center">
                { action }
            </div>
        </div>
    );
}

export default GrammarRuleCard;
