import { JSX } from 'preact';

type CardProps = {
    children: JSX.Element | string;
}

const Card = (props: CardProps) => {
    return (
        <div class="flex m-2 py-4 px-8 bg-white hover:shadow-xl shadow-lg rounded-lg items-center justify-center">
            {props.children}
        </div>
    )
}

export default Card;
