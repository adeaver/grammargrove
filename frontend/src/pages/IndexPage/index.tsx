import { useState } from 'preact/hooks';

import Input, { InputType } from '../../components/Input';
import Button from '../../components/Button';

import {
    searchByEmail,
    SearchByEmailAction,
    SearchByEmailResponse
} from './api';

const IndexPage = () => {
    const [ email, setEmail ] = useState<string>("");
    const [ password, setPassword ] = useState<string>("");
    const [ isLoading, setIsLoading ] = useState<boolean>(false);
    const [ error, setError ] = useState<Error | null>(null);
    const [ action, setAction ] = useState<SearchByEmailAction | null>(null);

    const handleClick = () => {
        setIsLoading(true);
        searchByEmail(
            email,
            (resp: SearchByEmailResponse) => {
                setIsLoading(false);
                setError(null);
                setAction(resp.action)
            },
            (err: Error) => {
                console.log("error");
                setIsLoading(false);
                setError(err);
                setAction(null)
            }
        );
    }

    if (isLoading || !!error) {
        return (
            <div className="w-full grid grid-cols-3">
                <div className="col-span-1">
                    {
                        !!error && (
                            <p>There was an error</p>
                        )
                    }
                    <Input
                        type={InputType.Email}
                        value={email}
                        placeholder="Email Address"
                        onChange={setEmail} />
                    <Button onClick={handleClick}>
                        Submit
                    </Button>
                </div>
            </div>
        );
    } else if (action == SearchByEmailAction.Redirect) {

    } else if (action == SearchByEmailAction.RequireLogin) {
        return (
            <div className="w-full grid grid-cols-3">
                <div className="col-span-1">
                    <form method="POST" action="/login">
                        <Input
                            type={InputType.Email}
                            value={email}
                            placeholder="Email Address"
                            onChange={setEmail} />
                        <Input
                            type={InputType.Password}
                            value={password}
                            placeholder="Password"
                            onChange={setPassword} />
                        <Button isSubmit>
                            Submit
                        </Button>
                    </form>
                </div>
            </div>
        );
    } else if (action == SearchByEmailAction.RequireSignup) {
        return (
            <div className="w-full grid grid-cols-3">
                <div className="col-span-1">
                    <p>An email has been sent to you</p>
                </div>
            </div>
        );
    } else {
        return (
            <div className="w-full grid grid-cols-3">
                <div className="col-span-1">
                    <Input
                        type={InputType.Email}
                        value={email}
                        placeholder="Email Address"
                        onChange={setEmail} />
                    <Button onClick={handleClick}>
                        Submit
                    </Button>
                </div>
            </div>
        );
    }
}

export default IndexPage;
