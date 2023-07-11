import Text from '../../components/Text';

type CheckboxProps = {
    name: string;
    label: string;
    className?: string;
    isChecked?: boolean;
    value: string;
    onChange: (value: string, isChecked: boolean) => void;
}

const Checkbox = (props: CheckboxProps) => {
    let className = !!props.className ? `${props.className} ` : "";
    if (props.isChecked) {
        className = `${className}right-0 border-primary-600`;
    }

    return (
        <div class="flex flex-row space-x-2 items-center">
            <CheckboxElement
                className={className}
                labelClassName={props.isChecked ? "bg-primary-600" : ""}
                name={props.name}
                label={props.label}
                value={props.value}
                onChange={props.onChange}
                isChecked={props.isChecked} />
            <label for={props.name}>
                <Text>
                    { props.label }
                </Text>
            </label>
        </div>
    )
}

type CheckboxElementProps = {
    labelClassName?: string;
} & CheckboxProps;

const CheckboxElement = (props: CheckboxElementProps) => {
    // @ts-ignore
    const handleChange = (event) => {
        props.onChange(event.target!.value, !props.isChecked);
    }

    return (
        <div class="relative inline-block w-10 mr-2 align-middle select-none transition duration-200 ease-in">
            <input
                class={`${props.className} absolute block w-6 h-6 rounded-full bg-white border-4 appearance-none cursor-pointer`}
                type="checkbox"
                name={props.name}
                value={props.value}
                onChange={handleChange}
                id={props.name} />
            <label
                class={`${props.labelClassName} block overflow-hidden h-6 rounded-full bg-gray-300 cursor-pointer`}
                for={props.name}>
            </label>
        </div>
    );
}

export default Checkbox;
