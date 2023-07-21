import { useState } from 'preact/hooks';

import Text, { TextType, TextAlignment, TextFunction } from '../../../components/Text';
import PageNavigationButtons from '../../../components/PageNavigationButtons';

import GrammarRuleSearch from '../../../components/GrammarRuleSearch';
import GrammarRuleCard from '../../../components/GrammarRuleSearch/GrammarRuleCard';

import {
    GrammarRule,
} from '../../../common/api';

import {
    UserGrammarRule,
} from '../../../common/api/uservocabulary';

type UserGrammarRulesDisplayProps = {
    grammarRules: UserGrammarRule[];

    handleAddUserGrammarRule: (u: UserGrammarRule) => void;
    handleRemoveUserGrammarRule: (uid: string) => void;

    getNextPage?: () => void;
    getPreviousPage?: () => void;
}

const UserGrammarRulesDisplay = (props: UserGrammarRulesDisplayProps) => {
    const [ searchResults, setSearchResults ] = useState<GrammarRule[]>([]);
    const [ searchResultError, setSearchResultError ] = useState<Error | null>(null);

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
                <PageNavigationButtons
                    getNextPage={props.getNextPage}
                    getPreviousPage={props.getPreviousPage} />
            </div>
            <hr class="my-4 border-2 border-slate-600" />
            {
                props.grammarRules.map((u: UserGrammarRule) => (
                    <GrammarRuleCard
                        key={u.id}
                        grammarRule={u.grammar_rule}
                        userGrammarRuleID={u.id}
                        handleAddUserGrammarRule={props.handleAddUserGrammarRule}
                        handleRemoveUserGrammarRule={props.handleRemoveUserGrammarRule} />
                ))
            }
            <Text alignment={TextAlignment.Left} type={TextType.SectionHeader}>
                Search for a new rule
            </Text>
            <GrammarRuleSearch
                onSuccess={setSearchResults}
                onError={setSearchResultError} />
            <GrammarRuleSearchBody
                searchResults={searchResults}
                searchResultError={searchResultError}
                handleAddUserGrammarRule={props.handleAddUserGrammarRule}
                handleRemoveUserGrammarRule={props.handleRemoveUserGrammarRule} />

        </div>
    )
}

type GrammarRuleSearchBodyProps = {
    searchResults: GrammarRule[];
    searchResultError: Error | null;
    handleRemoveUserGrammarRule?: (id: string) => void;
    handleAddUserGrammarRule?: (u: UserGrammarRule) => void;
}

const GrammarRuleSearchBody = (props: GrammarRuleSearchBodyProps) => {
    if (!!props.searchResultError) {
        return (
            <Text function={TextFunction.Warning}>
                Something went wrong.
            </Text>
        );
    }
    return (
        <div>
            {
                props.searchResults.map((g: GrammarRule) => (
                    <GrammarRuleCard
                        key={g.id}
                        grammarRule={g}
                        userGrammarRuleID={g.user_grammar_rule_entry}
                        handleAddUserGrammarRule={props.handleAddUserGrammarRule}
                        handleRemoveUserGrammarRule={props.handleRemoveUserGrammarRule} />

                ))
            }
        </div>
    )
}

export default UserGrammarRulesDisplay;
