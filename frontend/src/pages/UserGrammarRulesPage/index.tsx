import { useEffect, useState } from 'preact/hooks';

import {
    PaginatedResponse
} from '../../util/gfetch';

import Header from '../../components/Header';
import Text, { TextFunction } from '../../components/Text';
import LoadingIcon from '../../components/LoadingIcon';
import Link, { LinkTarget } from '../../components/Link';

import {
    UserGrammarRule,
    getUserGrammarRules,
} from '../../common/api/uservocabulary';

import UserGrammarRuleDisplay from './components/UserGrammarRuleDisplay';


const UserGrammarRulesPage = () => {
    const [ isLoading, setIsLoading ] = useState<boolean>(true);
    const [ userGrammarRules, setUserGrammarRules ] = useState<UserGrammarRule[]>([]);
    const [ error, setError ] = useState<Error | null>(null);
    const [ nextPage, setNextPage ] = useState<number | null | undefined>(undefined);
    const [ previousPage, setPreviousPage ] = useState<number | null | undefined>(undefined);

    const getUserGrammarRulesPage = (pageNumber: number | null | undefined) => {
        if (pageNumber === null) {
            return;
        }
        setIsLoading(true);
        getUserGrammarRules(
            pageNumber,
            (resp: PaginatedResponse<UserGrammarRule>) => {
                setIsLoading(false);
                setError(null);
                setPreviousPage(resp.previous);
                setNextPage(resp.next);
                setUserGrammarRules(resp.results);
            },
            (err: Error) => {
                setIsLoading(false);
                setError(err);
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
        getUserGrammarRulesPage(nextPage);
    }, []);

    let body;
    if (isLoading) {
        body = (
            <div class="w-full flex items-center justify-center">
                <LoadingIcon />
            </div>
        );
    } else if (!!error) {
        body = (
            <div class="w-full flex items-center justify-center">
                <Text function={TextFunction.Warning}>
                    Something went wrong, try again later.
                </Text>
            </div>
        );
    } else {
        body = (
            <div class="w-full">
                <UserGrammarRuleDisplay
                    grammarRules={userGrammarRules}
                    getNextPage={makeChangeUserGrammarRulesPageFunc(nextPage)}
                    getPreviousPage={makeChangeUserGrammarRulesPageFunc(previousPage)}
                    handleAddUserGrammarRule={handleAddUserGrammarRule}
                    handleRemoveUserGrammarRule={handleRemoveUserGrammarRule} />
            </div>
        )
    }
    return (
        <div>
            <Header />
            <div class="flex flex-col space-y-2">
                <Text>
                    Need to update your vocabulary words?
                </Text>
                <Link target={LinkTarget.Self} href="/vocabulary/">
                    Click here
                </Link>
            </div>
            { body }
            <Link target={LinkTarget.Self} href="/dashboard/">
                Back to the dashboard
            </Link>
        </div>
    );
}

export default UserGrammarRulesPage;
