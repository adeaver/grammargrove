export enum InputType {
    Password = 'password',
    Email = 'email',
    Text = 'text'
}

type InputProps = {
    type: InputType;
    value: string;
    onChange: (v: string) => void;
}

const Input = (props: InputProps) => {
    // @ts-ignore
    const handleChange = (event) => {
        props.onChange(event.target!.value);
    }

    return (
        <input
            type={props.type}
            value={props.value}
            onChange={handleChange} />
    )
}

export default Input;
