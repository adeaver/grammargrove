import { useState } from 'preact/hooks';

import Input, { InputType } from '../../components/Input';
import Button from '../../components/Button';

import {
    searchForWord,
    SearchForWordResponse,
    SearchResult,
} from './api';

const Dashboard = () => {
    const [ searchQuery, setSearchQuery ] = useState<string>("");
    const [ searchResults, setSearchResults ] = useState<SearchResult[]>([]);
    const [ isLoading, setIsLoading ] = useState<boolean>(false);
    const [ error, setError ] = useState<Error | null>(null);

    const handleSubmit = () => {
        setIsLoading(true);
        searchForWord(
            searchQuery, undefined,
            (resp: SearchForWordResponse) => {
                setIsLoading(false);
                if (!resp.success) {
                    setError(new Error("Bad request"));
                    setSearchResults([]);
                    return
                }
                setError(null);
                setSearchResults(resp.results);
            },
            (err: Error) => {
                setIsLoading(false);
                setError(err);
                setSearchResults([]);
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
            {
                searchResults.map((s: SearchResult) => (
                    <p key={s.word_id}>{s.display}</p>
                ))
            }
        </div>
    )
}

export default Dashboard;
