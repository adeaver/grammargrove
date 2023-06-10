import { JSX } from 'preact';

type ButtonProps = {
    onClick?: () => void;
    children?: JSX.Element | string;
    isSubmit?: boolean;
}

const Button = (props: ButtonProps) => {
    if (props.isSubmit) {
        <button type="submit">
            { props.children }
        </button>
    } else if (!props.onClick) {
        throw Error("OnClick not defined")
    }
    return (
        <button onClick={props.onClick}>
            { props.children }
        </button>
    )
}

export default Button;
