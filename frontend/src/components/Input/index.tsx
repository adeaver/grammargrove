export enum InputType {
    Password = 'password',
    Email = 'email',
    Text = 'text',
    Hidden = 'hidden'
}

type InputProps = {
    type: InputType;
    value: string;
    onChange: (v: string) => void;
    name: string;
    placeholder?: string;
}

const Input = (props: InputProps) => {
    // @ts-ignore
    const handleChange = (event) => {
        props.onChange(event.target!.value);
    }

    return (
        <input
            className="p-2 text-xl border border-slate-600 rounded-md"
            type={props.type}
            value={props.value}
            name={props.name}
            placeholder={props.placeholder || ""}
            onChange={handleChange} />
    )
}

export default Input;
