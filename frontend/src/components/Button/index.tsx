import { JSX } from 'preact';

export enum ButtonType {
    Primary = 'primary',
    Secondary = 'secondary',
    Warning = 'warning',
    Confirmation = 'confirmation'
}

type ButtonProps = {
    onClick?: () => void;
    children?: JSX.Element | string;
    isSubmit?: boolean;
    isLoading?: boolean;
    isDisabled?: boolean;
    type?: ButtonType;
}

const getButtonColorsByType = (type: ButtonType | undefined) => {
    switch (type) {
        case undefined:
        case ButtonType.Primary:
            return 'border-primary-600 bg-primary-600 hover:bg-primary-700 text-white';
        case ButtonType.Secondary:
            return 'border-primary-600 bg-white hover:bg-primary-700 text-primary-600 hover:text-white';
        case ButtonType.Warning:
            return 'border-warning-600 bg-warning-600 hover:bg-warning-700 text-white';
        case ButtonType.Confirmation:
            return 'border-confirmation-600 bg-confirmation-600 hover:bg-confirmation-700 text-white';
        default:
            throw new Error(`Unrecognized button type ${type}`);
    }
}

const Button = (props: ButtonProps) => {
    // TODO: add loading spinner
    const colors = getButtonColorsByType(props.type);
    if (props.isSubmit) {
        <button
            className={`w-full border ${colors} rounded-md px-4 py-2 m-2 transition duration-500 ease select-none focus:outline-none focus:shadow-outline font-body`}
            type="submit"
            disabled={props.isDisabled || props.isLoading}>
            { props.children }
        </button>
    } else if (!props.onClick) {
        throw Error("OnClick not defined")
    }
    return (
        <button
            className={`w-full border ${colors} rounded-md px-4 py-2 transition duration-500 ease select-none focus:outline-none focus:shadow-outline font-body`}
            onClick={props.onClick}
            disabled={props.isDisabled || props.isLoading}>
            { props.children }
        </button>
    )
}

export default Button;
