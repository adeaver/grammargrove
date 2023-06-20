import { useState } from 'preact/hooks';

import GrammarRuleSearch from '../../../components/GrammarRuleSearch';
import { GrammarRule } from '../../../common/api';
import GrammarRuleCard from '../../../components/GrammarRuleSearch/GrammarRuleCard';

import {
    UserGrammarRule,
    addUserGrammarRule,
    deleteUserGrammarRule,
} from '../api';

type GrammarRuleSearchProps = {
    userGrammarRulesByID: { [key: string]: UserGrammarRule };
    loadingGrammarRules: { [key: string]: boolean };

    setUserGrammarRulesByID: (userGrammarRulesByID: { [key: string]: UserGrammarRule }) => void;
    setLoadingGrammarRules: (loadingGrammarRules: { [key: string]: boolean }) => void;
    setError: (err: Error | null) => void;
}

const GrammarRuleSearchComponent = (props: GrammarRuleSearchProps) => {
    const [ searchResults, setSearchResults ] = useState<GrammarRule[]>([]);
    const [ error, setError ] = useState<Error | null>(null);

    const handleLoadingGrammarRule = (grammarRuleID: string, isLoading: boolean) => {
        if (isLoading) {
            props.setLoadingGrammarRules({
                ...props.loadingGrammarRules,
                [grammarRuleID]: true,
            });
        } else {
            props.setLoadingGrammarRules(
                Object.keys(props.loadingGrammarRules).reduce(
                    (acc: { [key: string]: boolean }, curr: string) => {
                        if (curr == grammarRuleID) {
                            return acc
                    }
                    return {
                        ...acc,
                        [grammarRuleID]: true,
                    }
                }, {})
            );
        }
    }

    const handleAddUserGrammarRule = (grammarRuleID: string) => {
        handleLoadingGrammarRule(grammarRuleID, true);
        addUserGrammarRule(
            grammarRuleID, null,
            (resp: UserGrammarRule) => {
                handleLoadingGrammarRule(grammarRuleID, false);
                props.setUserGrammarRulesByID({
                    ...props.userGrammarRulesByID,
                    [resp.grammar_rule.id]: resp,
                })
                props.setError(null);
            },
            (err: Error) => {
                handleLoadingGrammarRule(grammarRuleID, false);
                props.setError(err);
            }
        );
    }

    const handleDeleteUserGrammarRule = (grammarRuleID: string) => {
        handleLoadingGrammarRule(grammarRuleID, true);
        const id: string | null = props.userGrammarRulesByID[grammarRuleID].id || null;
        if (!id) {
            handleLoadingGrammarRule(grammarRuleID, false);
            return;
        }
        deleteUserGrammarRule(
            id,
            () => {
                handleLoadingGrammarRule(grammarRuleID, false);
                props.setUserGrammarRulesByID(
                    Object.keys(props.userGrammarRulesByID).reduce(
                        (acc: { [key: string]: UserGrammarRule }, currValue: string) => {
                            if (currValue === grammarRuleID) {
                                return acc;
                            }
                            return {
                                ...acc,
                                [currValue]: props.userGrammarRulesByID[currValue],
                            }
                        }, {})
                )
                props.setError(null);
            },
            (err: Error) => {
                handleLoadingGrammarRule(grammarRuleID, false);
                props.setError(err);
            }
        );
    }

    return (
        <div>
            { !!error && <p>There was an error</p> }
            <GrammarRuleSearch
               onSuccess={setSearchResults}
               onError={setError } />
            {
                !error && searchResults.map((s: GrammarRule) => {
                    let action;
                    if (!props.userGrammarRulesByID[s.id]) {
                        action = {
                            text: 'Add grammar rule to your list',
                            action: (s: GrammarRule) => { handleAddUserGrammarRule(s.id) },
                        }
                    } else {
                        action = {
                            text: 'Remove grammar rule from your list',
                            action: (s: GrammarRule) => { handleDeleteUserGrammarRule(s.id) },
                        }
                    }
                    return (
                        <GrammarRuleCard
                            grammarRule={s}
                            action={action}
                            isLoading={props.loadingGrammarRules[s.id]} />
                    )
                })
            }
        </div>
    )
}

export default GrammarRuleSearchComponent;
