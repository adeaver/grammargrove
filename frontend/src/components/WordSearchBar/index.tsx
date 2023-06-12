import { useState } from 'preact/hooks';

import Input, { InputType } from '../Input';
import Button from '../Button';

import {
    searchForWord,
    SearchForWordResponse,
    SearchResult,
} from './api';

type WordSearchBarProps = {
    onSuccess: (s: SearchResult[]) => void;
    onError?: (err: Error | null) => void;
}

const WordSearchBar = (props: WordSearchBarProps) => {
    const [ searchQuery, setSearchQuery ] = useState<string>("");
    const [ isLoading, setIsLoading ] = useState<boolean>(false);
    const [ error, setError ] = useState<Error | null>(null);

    const handleError = (err: Error | null) => {
        setError(err);
        !!props.onError && props.onError(err);
    }

    const handleSubmit = () => {
        setIsLoading(true);
        searchForWord(
            searchQuery, undefined,
            (resp: SearchForWordResponse) => {
                setIsLoading(false);
                if (!resp.success) {
                    handleError(new Error("Bad request"));
                    return
                }
                handleError(null);
                props.onSuccess(resp.results);
            },
            (err: Error) => {
                setIsLoading(false);
                handleError(err);
            }
        );
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
        </div>
    );
}

export default WordSearchBar;
