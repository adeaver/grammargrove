import { useState } from 'preact/hooks';

import { PaginatedResponse } from '../../util/gfetch';

import Input, { InputType } from '../Input';
import Button, { ButtonType } from '../Button';
import Text, { TextFunction } from '../../components/Text';
import LoadingIcon from '../../components/LoadingIcon';

import { GrammarRule } from '../../common/api';

import {
    searchForGrammarRule,
} from './api';

type GrammarRuleSearchProps = {
    onSuccess: (s: GrammarRule[]) => void;
    onError: (err: Error) => void;
}

const GrammarRuleSearch = (props: GrammarRuleSearchProps) => {
    const [ searchQuery, setSearchQuery ] = useState<Array<string | null>>([null]);
    const [ isLoading, setIsLoading ] = useState<boolean>(false);
    const [ error, setError ] = useState<Error | null>(null);

    const handleAddWordToSearchQuery = () => {
        setSearchQuery(searchQuery.concat(null));
    }

    const [ pageTurnSearchQuery, setPageTurnSearchQuery ] = useState<Array<string | null>>([]);

    const [ nextPage, setNextPage ] = useState<number | null>(null);
    const [ previousPage, setPreviousPage ] = useState<number | null>(null);

    const getPageFunc = (page: number | null) => {
        if (page == null) {
            return null;
        }
        return () => {
            handleSearch(pageTurnSearchQuery, page);
        }
    }

    const handleUpdateSearchQuery = (idx: number) => {
        return (value: string) => {
            setSearchQuery(
                searchQuery.map((currValue: string | null, currIdx: number) => {
                    return currIdx === idx ? value : currValue;
                })
            );
        }
    }

    const handleRemoveSearchQuery = (idx: number) => {
        return () => {
            setSearchQuery(
                searchQuery.filter((_: string | null, currIdx: number) => currIdx !== idx)
            );
        }
    }

    const handleSearch = (query: Array<string | null>, pageNumber: number | null) => {
        setIsLoading(true);
        searchForGrammarRule(
            query.filter((value: string | null) => !!value) as string[],
            pageNumber,
            (resp: PaginatedResponse<GrammarRule>) => {
                setIsLoading(false);
                setError(null);
                props.onSuccess(resp.results);
                setNextPage(resp.next);
                setPreviousPage(resp.previous);
                setPageTurnSearchQuery(query);
            },
            (err: Error) => {
                setIsLoading(false);
                setError(err);
                props.onError(err);
            }
        );
    }

    const getNextPage = getPageFunc(nextPage);
    const getPreviousPage = getPageFunc(previousPage);

    const handleSubmit = () => {
        handleSearch(searchQuery, null);
    }

    if (isLoading) {
        return <LoadingIcon />;
    }
    return (
        <div>
            {
                !!error && (
                    <Text function={TextFunction.Warning}>
                        Something went wrong, try again later.
                    </Text>
                )
            }
            <div class="grid grid-cols-4">
            {
                searchQuery.map((value: string | null, idx: number) => {
                    const tag = `${Math.floor(Math.random() * 2000) + 1}`;
                    return (
                        <div class="p-4 col-span-4 md:col-span-1">
                            <Input
                                type={InputType.Text}
                                value={!!value ? value : ""}
                                key={`search-query-${tag}`}
                                placeholder="Add Search Term"
                                name={`search-query-${tag}`}
                                onChange={handleUpdateSearchQuery(idx)} />
                            <Button className="my-2" onClick={handleRemoveSearchQuery(idx)}>
                                Remove this term
                            </Button>
                        </div>
                    )
                })
            }
            </div>
            <div class="flex flex-row space-x-4 my-2">
                <Button onClick={handleSubmit}>
                    Search
                </Button>
                <Button type={ButtonType.Secondary} onClick={handleAddWordToSearchQuery}>
                    Add Word
                </Button>
            </div>
            <div class="grid grid-cols-2 gap-4">
            {
                !!previousPage ? (
                    <Button type={ButtonType.Secondary} onClick={getPreviousPage!}>
                        Previous Page
                    </Button>
                ) : (
                    <div />
                )
            }
            {
                !!nextPage ? (
                    <Button type={ButtonType.Secondary} onClick={getNextPage!}>
                        Next Page
                    </Button>
                ) : (
                    <div />
                )
            }
            </div>
        </div>
    );
}

export default GrammarRuleSearch;
