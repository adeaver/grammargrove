import { useEffect, useState } from 'preact/hooks';

import {
    UserVocabulary,
    getUserVocabulary,

    UserGrammarRule,
    getUserGrammarRules,
} from '../../common/api/uservocabulary';

import GrammarRuleCard from '../../components/GrammarRuleSearch/GrammarRuleCard';
// import WordCard from '../../components/WordSearchBar/WordCard';

const UserVocabularyPage = () => {
    const [ userVocabulary, setUserVocabulary ] = useState<UserVocabulary[]>([]);
    const [ isLoadingUserVocabulary, setIsLoadingUserVocabulary ] = useState<boolean>(true);
    const [ userVocabularyError, setUserVocabularyError ] = useState<Error | null>(null);

    const [ userGrammarRules, setUserGrammarRules ] = useState<UserGrammarRule[]>([]);
    const [ isLoadingUserGrammarRules, setIsLoadingUserGrammarRules ] = useState<boolean>(true);
    const [ userGrammarRulesError, setUserGrammarRulesError ] = useState<Error | null>(null);

    useEffect(() => {
        getUserVocabulary(
            (resp: UserVocabulary[]) => {
                setIsLoadingUserVocabulary(false);
                setUserVocabulary(resp);
                setUserVocabularyError(null);
            },
            (err: Error) => {
                setIsLoadingUserVocabulary(false);
                setUserVocabulary([]);
                setUserVocabularyError(err);
            }
        );
        getUserGrammarRules(
            (resp: UserGrammarRule[]) => {
                setIsLoadingUserGrammarRules(false);
                setUserGrammarRulesError(null);
                setUserGrammarRules(resp);
            },
            (err: Error) => {
                setIsLoadingUserGrammarRules(false);
                setUserGrammarRulesError(err);
                setUserGrammarRules([]);
            }
        );
    }, []);

    if (isLoadingUserGrammarRules || isLoadingUserVocabulary) {
        return (
            <div>Loading...</div>
        );
    } else if (!!userGrammarRulesError || !!userVocabularyError) {
        return (
            <div>Something went wrong</div>
        );
    }
    return (
        <div>
            <p>Vocabulary words</p>
            {
                userVocabulary.map((u: UserVocabulary) => (
                    <p>{u.id}</p>
                ))
            }
            <p>Grammar rules</p>
            {
                userGrammarRules.map((g: UserGrammarRule) => (
                    <GrammarRuleCard
                        key={g.id}
                        grammarRule={g.grammar_rule} />
                ))
            }
        </div>
    );
}

export default UserVocabularyPage;
