export enum InputType {
    Password = 'password',
    Email = 'email',
    Text = 'text',
    Hidden = 'hidden',
    Number = 'number'
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
        <div class="w-full">
            {
                !!props.placeholder && (
                    <label
                        for={props.name}
                        className="w-full text-sm text-text-700 font-body font-bold">
                        { props.placeholder }
                    </label>
                )
            }
            <input
                className="mt-2 flex h-12 w-full items-center justify-center rounded-xl border bg-white/0 p-3 text-sm outline-none border-gray-200 font-body text-text-700"
                type={props.type}
                value={props.value}
                name={props.name}
                id={props.name}
                onChange={handleChange} />
        </div>
    )
}

export default Input;
