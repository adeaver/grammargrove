import { useState } from 'preact/hooks';

import Input, { InputType } from '../Input';
import Button from '../Button';

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

    const handleError = (err: Error | null) => {
        setError(err);
        !!props.onError && props.onError(err);
    }

    const handleSubmit = () => {
        setIsLoading(true);
        searchForWord(
            searchQuery, undefined,
            (resp: Word[]) => {
                setIsLoading(false);
                handleError(null);
                props.onSuccess(resp);
            },
            (err: Error) => {
                setIsLoading(false);
                props.onSuccess([]);
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
