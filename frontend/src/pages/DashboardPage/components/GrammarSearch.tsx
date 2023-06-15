import { useState } from 'preact/hooks';

import GrammarRuleSearch from '../../../components/GrammarRuleSearch';
import { SearchResult } from '../../../components/GrammarRuleSearch/api';
import GrammarRuleCard from '../../../components/GrammarRuleSearch/GrammarRuleCard';

const GrammarRuleSearchComponent = () => {
    const [ searchResults, setSearchResults ] = useState<SearchResult[]>([]);
    const [ error, setError ] = useState<Error | null>(null);

    return (
        <div>
            { !!error && <p>There was an error</p> }
            <GrammarRuleSearch
               onSuccess={setSearchResults}
               onError={setError } />
            {
                !error && searchResults.map((s: SearchResult) => (
                    <GrammarRuleCard grammarRule={s} />
                ))
            }
        </div>
    )
}

export default GrammarRuleSearchComponent;
