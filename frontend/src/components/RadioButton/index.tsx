type RadioButtonProps = {
    className?: string;
    isSelected?: boolean;
}

const RadioButton = (props: RadioButtonProps) => {
    const fillColor = props.isSelected ? 'fill-primary-600' : 'fill-zinc-500';
    let className = `${fillColor} max-h-9 min-h-9 h-9 max-h-w min-w-9 w-9`;
    if (props.className) {
        className = `${props.className} ${className}`;
    }

    return (
        <svg xmlns="http://www.w3.org/2000/svg" class={className} viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
        </svg>
    )
}

export default RadioButton;
