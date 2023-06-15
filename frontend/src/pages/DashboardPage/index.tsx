import { useEffect, useState } from 'preact/hooks';

import {
    UserVocabulary,
    getUserVocabulary,

    UserGrammarRule,
    getUserGrammarRules,
} from './api';

import WordSearch from './components/WordSearch';
import GrammarSearch from './components/GrammarSearch';

const Dashboard = () => {
    const [ isLoadingWords, setIsLoadingWords ] = useState<boolean>(true);
    const [ loadingWords, setLoadingWords ] = useState<{ [key: string]: boolean }>({});
    const [ userVocabularyByWordID, setUserVocabularyByWordID ] = useState<{ [word_id: string]: UserVocabulary }>({});

    const [ isLoadingGrammarRules, setIsLoadingGrammarRules ] = useState<boolean>(true);
    const [ loadingGrammarRules, setLoadingGrammarRules ] = useState<{ [key: string]: boolean }>({});
    const [ userGrammarRulesByID, setUserGrammarRulesByID ] = useState<{ [key: string]: UserGrammarRule }>({});

    const [ error, setError ] = useState<Error | null>(null);

    useEffect(() => {
        getUserVocabulary(
            (resp: UserVocabulary[]) => {
                setIsLoadingWords(false);
                setUserVocabularyByWordID(
                    resp.reduce((acc: { [word: string]: UserVocabulary }, curr: UserVocabulary) => ({
                        ...acc,
                        [curr.word]: curr,
                    }), {})
                );
            },
            (err: Error) => {
                setIsLoadingWords(false);
                setError(err);
            }
        );
        getUserGrammarRules(
            (resp: UserGrammarRule[]) => {
                setIsLoadingGrammarRules(false);
                setUserGrammarRulesByID(
                    resp.reduce(
                        (acc: { [key: string]: UserGrammarRule }, curr: UserGrammarRule) => ({
                            ...acc,
                            [curr.grammar_rule]: curr,
                        }), {})
                )
            },
            (err: Error) => {
                setIsLoadingGrammarRules(false);
                setError(err);
            }
        );
    }, []);


    if (!!error) {
        return (
            <div>
                An error occurred. Try again later.
            </div>
        )
    } else if (isLoadingWords || isLoadingGrammarRules) {
        // Entire page is loading
        return (
            <div>
                Loading ...
            </div>
        )
    }
    return (
        <div>
            <WordSearch
                userVocabularyByWordID={userVocabularyByWordID}
                loadingWords={loadingWords}
                setUserVocabularyByWordID={setUserVocabularyByWordID}
                setLoadingWords={setLoadingWords}
                setError={setError} />
            <GrammarSearch
                userGrammarRulesByID={userGrammarRulesByID}
                setUserGrammarRulesByID={setUserGrammarRulesByID}
                loadingGrammarRules={loadingGrammarRules}
                setLoadingGrammarRules={setLoadingGrammarRules}
                setError={setError} />
        </div>
    )
}

export default Dashboard;
