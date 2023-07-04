export enum InputType {
    Password = 'password',
    Email = 'email',
    Text = 'text',
    Hidden = 'hidden',
    Number = 'number',
    TextArea = 'textarea',
}

type InputProps = {
    type: InputType;
    value: string;
    onChange: (v: string) => void;
    name: string;
    placeholder?: string;
    disabled?: boolean;
    rows?: number;
}

const Input = (props: InputProps) => {
    // @ts-ignore
    const handleChange = (event) => {
        props.onChange(event.target!.value);
    }

    const className = "mt-2 flex h-12 w-full items-center justify-center rounded-xl border bg-white/0 p-3 text-sm outline-none border-gray-400 font-body text-text-700";
    let body;
    if (props.type === InputType.TextArea) {
        body = (
            <textarea
                className={`${className} resize-none`}
                value={props.value}
                name={props.name}
                disabled={!!props.disabled}
                id={props.name}
                rows={props.rows == null ? 4 : props.rows}
                onChange={handleChange}>
            </textarea>
        );
    } else {
        body = (
            <input
                className={className}
                type={props.type}
                value={props.value}
                name={props.name}
                disabled={!!props.disabled}
                id={props.name}
                onChange={handleChange} />
        );
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
            { body }
        </div>
    )
}

export default Input;
