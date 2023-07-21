import { useEffect, useState } from 'preact/hooks';

import {
    PaginatedResponse
} from '../../util/gfetch';

import Header from '../../components/Header';
import Text, { TextFunction } from '../../components/Text';
import LoadingIcon from '../../components/LoadingIcon';

import {
    UserVocabulary,
    getUserVocabulary,
} from '../../common/api/uservocabulary';

import UserVocabularyDisplay from './components/UserVocabularyDisplay';

const UserVocabularyPage = () => {
    const [ isLoading, setIsLoading ] = useState<boolean>(true);
    const [ error, setError ] = useState<Error | null>(null);
    const [ nextPage, setNextPage ] = useState<number | null | undefined>(undefined);
    const [ previousPage, setPreviousPage ] = useState<number | null | undefined>(undefined);

    const [ userVocabulary, setUserVocabulary ] = useState<UserVocabulary[]>([]);

    const getUserVocabularyPage = (pageNumber: number | null | undefined) => {
        if (pageNumber === null) {
            return;
        }
        setIsLoading(true);
        getUserVocabulary(
            pageNumber,
            (resp: PaginatedResponse<UserVocabulary>) => {
                setIsLoading(false);
                setError(null);
                setPreviousPage(resp.previous);
                setNextPage(resp.next);
                setUserVocabulary(resp.results);
            },
            (err: Error) => {
                setIsLoading(false);
                setError(err);
            }
        );
    }

    useEffect(() => {
        getUserVocabularyPage(nextPage);
    }, []);

    const makeChangePageFunc = (pageNumber: number | undefined | null) => {
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
            <UserVocabularyDisplay
                isLoading={isLoading}
                vocabulary={userVocabulary}
                removeFromUserVocabulary={removeFromUserVocabulary}
                handleAddUserVocabulary={handleAddToUserVocabulary}
                getNextPage={makeChangePageFunc(nextPage)}
                getPreviousPage={makeChangePageFunc(previousPage)} />
        );
    }

    return (
        <div>
            <Header />
            { body }
        </div>
    );
}

export default UserVocabularyPage;
