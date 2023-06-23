import { useState } from 'preact/hooks';

import Input, { InputType } from '../Input';
import Button, { ButtonType } from '../Button';

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

    const handleSubmit = () => {
        setIsLoading(true);
        searchForGrammarRule(
            searchQuery.filter((value: string | null) => !!value) as string[],
            (resp: GrammarRule[]) => {
                setIsLoading(false);
                setError(null);
                props.onSuccess(resp);
            },
            (err: Error) => {
                setIsLoading(false);
                setError(err);
                props.onError(err);
            }
        );
    }

    if (isLoading) {
        return <p>Loading ...</p>
    }
    return (
        <div>
            {
                !!error && (
                    <p>There was an error</p>
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
                            <Button onClick={handleRemoveSearchQuery(idx)}>
                                Remove this term
                            </Button>
                        </div>
                    )
                })
            }
            </div>
            <div class="flex flex-row space-x-4">
                <Button type={ButtonType.Secondary} onClick={handleAddWordToSearchQuery}>
                    <p class="font-body">Add Word</p>
                </Button>
                <Button onClick={handleSubmit}>
                    Search
                </Button>
            </div>
        </div>
    );
}

export default GrammarRuleSearch;
