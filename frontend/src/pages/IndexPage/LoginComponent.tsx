import { useState } from 'preact/hooks';

import Text, { TextFunction } from '../../components/Text';
import Input, { InputType } from '../../components/Input';
import Button from '../../components/Button';
import { getCSRFToken } from '../../util/gfetch';
import { setLocation } from '../../util/window';

import {
    searchByEmail,
    SearchByEmailAction,
    SearchByEmailResponse
} from './api';

const LoginComponent = () => {
    const [ email, setEmail ] = useState<string>("");
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

    if (isLoading) {
        return (
            <Text>Loading...</Text>
        )
    } else if (action == SearchByEmailAction.Redirect) {
        // There's weirdly a bit of nuance here in that
        // Letting this fall through allows the back button
        // to properly render this page
        setLocation("/dashboard/");
    } else if (action == SearchByEmailAction.RequireLogin) {
        return (
            <LoginForm
                email={email}
                setEmail={setEmail} />
        );
    } else if (action == SearchByEmailAction.RequireSignup) {
        return (
            <Text>We sent you an email to access your account. Check your inbox for a magic link.</Text>
        );
    }
    return (
        <GenericEmailForm
            error={!!error ? "There was an error" : null }
            email={email}
            setEmail={setEmail}
            handleSubmit={handleClick} />
    );
}

type GenericEmailFormProps = {
    email: string;
    setEmail: (e: string) => void;
    handleSubmit: () => void;
    error: string | null;
}

const GenericEmailForm = (props: GenericEmailFormProps) => {
    return (
        <div className="w-full flex flex-col">
            {
                !!props.error && (
                    <Text function={TextFunction.Warning}>
                        There was an error processing your request. Try again later.
                    </Text>
                )
            }
            <div className="w-full flex flex-col justify-center items-center">
                <Input
                    type={InputType.Email}
                    value={props.email}
                    name="email"
                    placeholder="Email Address"
                    onChange={props.setEmail} />
                <div className="w-1/2 my-2">
                    <Button onClick={props.handleSubmit}>
                        Get Started
                    </Button>
                </div>
            </div>
        </div>
    )
}

type LoginFormProps = {
    email: string;
    setEmail: (e: string) => void;
}

const LoginForm = (props: LoginFormProps) => {
    const csrfToken = getCSRFToken();

    const [ password, setPassword ] = useState<string>("");

    return (
        <div className="w-full">
            <form method="POST" action="/login/">
                <Input
                    type={InputType.Hidden}
                    value={csrfToken || ""}
                    name="csrfmiddlewaretoken"
                    onChange={() => {}} />
                <Input
                    type={InputType.Email}
                    value={props.email}
                    name="email"
                    placeholder="Email Address"
                    onChange={props.setEmail} />
                <Input
                    type={InputType.Password}
                    value={password}
                    name="password"
                    placeholder="Password"
                    onChange={setPassword} />
                <Button className="my-2" isSubmit>
                    Submit
                </Button>
            </form>
        </div>
    );
}

export default LoginComponent;
