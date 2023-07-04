import { ComponentChildren } from 'preact';

type CardProps = {
    className?: string;
    children: ComponentChildren;
}

const Card = (props: CardProps) => {
    let className = "m-2 py-4 px-8 bg-white hover:shadow-xl shadow-lg rounded-lg";
    if (props.className) {
        className = `${props.className} ${className}`;
    }
    return (
        <div class={className}>
            {props.children}
        </div>
    )
}

export default Card;
