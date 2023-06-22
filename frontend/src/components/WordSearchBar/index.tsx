import { useState } from 'preact/hooks';

import Input, { InputType } from '../Input';
import Button, { ButtonType } from '../Button';

import { PaginatedResponse } from '../../util/gfetch'
import { Word } from '../../common/api';

import {
    searchForWord,
} from './api';

type WordSearchBarProps = {
    onSuccess: (s: Word[]) => void;
    onError?: (err: Error | null) => void;
}

const WordSearchBar = (props: WordSearchBarProps) => {
    const [ searchQuery, setSearchQuery ] = useState<string>("");
    const [ isLoading, setIsLoading ] = useState<boolean>(false);
    const [ error, setError ] = useState<Error | null>(null);

    const [ pageTurnSearchQuery, setPageTurnSearchQuery ] = useState<string>("");

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

    const handleError = (err: Error | null) => {
        setError(err);
        !!props.onError && props.onError(err);
    }

    const handleSearch = (query: string, page: number | null) => {
        setIsLoading(true);
        searchForWord(
            searchQuery, undefined, page,
            (resp: PaginatedResponse<Word>) => {
                setIsLoading(false);
                handleError(null);
                props.onSuccess(resp.results);
                setNextPage(resp.next);
                setPreviousPage(resp.previous);
                setPageTurnSearchQuery(query);
            },
            (err: Error) => {
                setIsLoading(false);
                props.onSuccess([]);
                handleError(err);
            }
        );
    }

    const getNextPage = getPageFunc(nextPage);
    const getPreviousPage = getPageFunc(previousPage);

    const handleSubmit = () => {
        handleSearch(searchQuery, null);
    }


    return (
        <div>
            {
                !!isLoading && (
                    <p>Loading...</p>
                )
            }
            {
                !!error && (
                    <p>There was an error</p>
                )
            }
            <Input
                type={InputType.Text}
                name="search"
                value={searchQuery}
                placeholder="Search for a word using Hanzi or Pinyin"
                onChange={setSearchQuery} />
            <Button onClick={handleSubmit}>
                Submit
            </Button>
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

export default WordSearchBar;
