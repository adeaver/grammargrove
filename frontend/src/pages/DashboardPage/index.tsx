import { useEffect, useState } from 'preact/hooks';

import {
    PaginatedResponse
} from '../../util/gfetch';
import {
    setLocation
} from '../../util/window';

import Header from '../../components/Header';
import Button from '../../components/Button';
import Text from '../../components/Text';

import {
    UserVocabulary,
    getUserVocabulary,

    UserGrammarRule,
    getUserGrammarRules,
} from '../../common/api/uservocabulary';

import UserVocabularyDisplay from './components/UserVocabularyDisplay';
import UserGrammarRuleDisplay from './components/UserGrammarRuleDisplay';

const DashboardPage = () => {
    const [ isLoadingUserVocabulary, setIsLoadingUserVocabulary ] = useState<boolean>(true);
    const [ userVocabulary, setUserVocabulary ] = useState<UserVocabulary[]>([]);
    const [ userVocabularyError, setUserVocabularyError ] = useState<Error | null>(null);
    const [ nextUserVocabularyPage, setNextUserVocabularyPage ] = useState<number | null | undefined>(undefined);
    const [ previousUserVocabularyPage, setPreviousUserVocabularyPage ] = useState<number | null | undefined>(undefined);

    const getUserVocabularyPage = (pageNumber: number | null | undefined) => {
        if (pageNumber === null) {
            return;
        }
        setIsLoadingUserVocabulary(true);
        getUserVocabulary(
            pageNumber,
            (resp: PaginatedResponse<UserVocabulary>) => {
                setIsLoadingUserVocabulary(false);
                setUserVocabularyError(null);
                setPreviousUserVocabularyPage(resp.previous);
                setNextUserVocabularyPage(resp.next);
                setUserVocabulary(resp.results);
            },
            (err: Error) => {
                setIsLoadingUserVocabulary(false);
                setUserVocabularyError(err);
            }
        );
    }

    const makeChangeUserVocabularyPageFunc = (pageNumber: number | undefined | null) => {
        if (pageNumber === null) {
            return undefined;
        }
        return () => {
            getUserVocabularyPage(pageNumber);
        }
    }

    const removeFromUserVocabulary = (userVocabularyID: string) => {
        setUserVocabulary(userVocabulary.filter((u: UserVocabulary) => u.id !== userVocabularyID));
    }
    const handleAddToUserVocabulary = (newVocabularyWord: UserVocabulary) => {
        const vocabulary = userVocabulary.filter((u: UserVocabulary) => u.id !== newVocabularyWord.id);
        vocabulary.unshift(newVocabularyWord)
        setUserVocabulary(vocabulary);
    }

    const [ isLoadingUserGrammarRules, setIsLoadingUserGrammarRules ] = useState<boolean>(true);
    const [ userGrammarRules, setUserGrammarRules ] = useState<UserGrammarRule[]>([]);
    const [ userGrammarRulesError, setUserGrammarRulesError ] = useState<Error | null>(null);
    const [ nextUserGrammarRulesPage, setNextUserGrammarRulesPage ] = useState<number | null | undefined>(undefined);
    const [ previousUserGrammarRulesPage, setPreviousUserGrammarRulesPage ] = useState<number | null | undefined>(undefined);

    const getUserGrammarRulesPage = (pageNumber: number | null | undefined) => {
        if (pageNumber === null) {
            return;
        }
        setIsLoadingUserVocabulary(true);
        getUserGrammarRules(
            pageNumber,
            (resp: PaginatedResponse<UserGrammarRule>) => {
                setIsLoadingUserGrammarRules(false);
                setUserGrammarRulesError(null);
                setPreviousUserGrammarRulesPage(resp.previous);
                setNextUserGrammarRulesPage(resp.next);
                setUserGrammarRules(resp.results);
            },
            (err: Error) => {
                setIsLoadingUserGrammarRules(false);
                setUserGrammarRulesError(err);
            }
        );
    }

    const makeChangeUserGrammarRulesPageFunc = (pageNumber: number | undefined | null) => {
        if (pageNumber === null) {
            return undefined;
        }
        return () => {
            getUserGrammarRulesPage(pageNumber);
        }
    }

    const handleAddUserGrammarRule = (u: UserGrammarRule) => {
        const toSet = userGrammarRules.filter((g: UserGrammarRule) => g.id !== u.id);
        toSet.unshift(u);
        setUserGrammarRules(toSet);
    }
    const handleRemoveUserGrammarRule = (uid: string) => {
        setUserGrammarRules(userGrammarRules.filter((g: UserGrammarRule) => g.id !== uid));
    }

    useEffect(() => {
        getUserVocabularyPage(nextUserVocabularyPage);
        getUserGrammarRulesPage(nextUserGrammarRulesPage);
    }, []);

    const navigateToQuizPage = () => {
        setLocation("/quiz/")
    }

    if (isLoadingUserGrammarRules) {
        return <p>Loading...</p>
    } else if (!!userVocabularyError || !!userGrammarRulesError) {
        return <p>Something went wrong</p>
    }
    return (
        <div>
            <Header />
            <div class="w-full flex items-center justify-center">
                <div class="max-w-lg flex flex-col space-y-4">
                    <Text>
                        Ready for a quiz?
                    </Text>
                    <Button onClick={navigateToQuizPage}>
                        Quiz me!
                    </Button>
                </div>
            </div>
            <UserVocabularyDisplay
                isLoading={isLoadingUserVocabulary}
                vocabulary={userVocabulary}
                removeFromUserVocabulary={removeFromUserVocabulary}
                handleAddUserVocabulary={handleAddToUserVocabulary}
                getNextPage={makeChangeUserVocabularyPageFunc(nextUserVocabularyPage)}
                getPreviousPage={makeChangeUserVocabularyPageFunc(previousUserVocabularyPage)} />
            <UserGrammarRuleDisplay
                grammarRules={userGrammarRules}
                getNextPage={makeChangeUserGrammarRulesPageFunc(nextUserGrammarRulesPage)}
                getPreviousPage={makeChangeUserGrammarRulesPageFunc(previousUserGrammarRulesPage)}
                handleAddUserGrammarRule={handleAddUserGrammarRule}
                handleRemoveUserGrammarRule={handleRemoveUserGrammarRule} />
        </div>
    );
}

export default DashboardPage;
