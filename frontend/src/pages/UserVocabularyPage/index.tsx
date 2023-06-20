import { useEffect, useState } from 'preact/hooks';

import {
    Word,
    GrammarRule
} from '../../common/api';

import {
    UserVocabulary,
    getUserVocabulary,
    deleteUserVocabulary,

    UserGrammarRule,
    getUserGrammarRules,
    deleteUserGrammarRule,
} from '../../common/api/uservocabulary';

import GrammarRuleCard from '../../components/GrammarRuleSearch/GrammarRuleCard';
import WordCard from '../../components/WordSearchBar/WordCard';

const UserVocabularyPage = () => {
    const [ userVocabulary, setUserVocabulary ] = useState<UserVocabulary[]>([]);
    const [ isLoadingUserVocabulary, setIsLoadingUserVocabulary ] = useState<boolean>(true);
    const [ loadingWords, setLoadingWords ] = useState<{ [key: string]: boolean }>({});
    const [ userVocabularyError, setUserVocabularyError ] = useState<Error | null>(null);

    const [ userGrammarRules, setUserGrammarRules ] = useState<UserGrammarRule[]>([]);
    const [ isLoadingUserGrammarRules, setIsLoadingUserGrammarRules ] = useState<boolean>(true);
    const [ loadingRules, setLoadingRules ] = useState<{ [key: string]: boolean }>({});
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

    const handleRemoveUserVocabulary = (u: UserVocabulary) => {
        setLoadingWords({
            ...loadingWords,
            [ u.id ]: true,
        });
        deleteUserVocabulary(
            u.id,
            () => {
                setLoadingWords({
                    ...loadingWords,
                    [ u.id ]: false,
                });
                setUserVocabularyError(null);
                setUserVocabulary(userVocabulary.filter((v: UserVocabulary) => v.id !== u.id ));
            },
            (err: Error) => {
                setLoadingWords({
                    ...loadingWords,
                    [ u.id ]: false,
                });
                setUserVocabularyError(err);
            }
        );
    }

    const handleRemoveGrammarRule = (g: UserGrammarRule) => {
        setLoadingRules({
            ...loadingRules,
            [g.id]: true
        });
        deleteUserGrammarRule(g.id,
            () => {
                setLoadingRules({
                    ...loadingRules,
                    [g.id]: false
                });
                setUserGrammarRulesError(null);
                setUserGrammarRules(userGrammarRules.filter((v: UserGrammarRule) => v.id !== g.id));
            },
            (err: Error) => {
                setLoadingRules({
                    ...loadingRules,
                    [g.id]: false
                });
                setUserGrammarRulesError(err);
            }
        );
    }

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
                    <WordCard
                        key={u.id}
                        word={u.word}
                        action={{
                            text: 'Remove from your list',
                            action: (_: Word) => { handleRemoveUserVocabulary(u) },
                        }}
                        isLoading={loadingWords[u.id]} />
                ))
            }
            <p>Grammar rules</p>
            {
                userGrammarRules.map((g: UserGrammarRule) => (
                    <GrammarRuleCard
                        key={g.id}
                        grammarRule={g.grammar_rule}
                        action={{
                            text: 'Remove from your list',
                            action: (_: GrammarRule) => { handleRemoveGrammarRule(g) },
                        }}
                        isLoading={loadingRules[g.id]} />
                ))
            }
        </div>
    );
}

export default UserVocabularyPage;
