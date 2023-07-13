import { ComponentChildren } from 'preact';

type FormProps = {
    className?: string;
    children: ComponentChildren;
    handleSubmit: () => void;
}

const Form = (props: FormProps) => {
    // @ts-ignore
    const handleSubmit = (event) => {
        event.preventDefault();
        props.handleSubmit();
    }

    return (
        <form className={props.className} onSubmit={handleSubmit} noValidate autoComplete="off">
            { props.children }
        </form>
    );
}

export default Form;
