import { JSX } from 'preact';

type ButtonProps = {
    onClick?: () => void;
    children?: JSX.Element | string;
    isSubmit?: boolean;
    isLoading?: boolean;
    isDisabled?: boolean;
}

const Button = (props: ButtonProps) => {
    // TODO: add loading spinner
    if (props.isSubmit) {
        <button type="submit"
            disabled={props.isDisabled || props.isLoading}>
            { props.children }
        </button>
    } else if (!props.onClick) {
        throw Error("OnClick not defined")
    }
    return (
        <button onClick={props.onClick}
            disabled={props.isDisabled || props.isLoading}>
            { props.children }
        </button>
    )
}

export default Button;
