import Text, { TextAlignment, TextFunction } from '../../components/Text';

export enum LinkTarget {
    Self = '_self',
    Blank = '_blank',
}

type LinkProps = {
    href: string;
    children: string;

    alignment?: TextAlignment;
    target?: LinkTarget;
}

const Link = (props: LinkProps) => {
    const target = !!props.target ? props.target : LinkTarget.Blank;

    return (
        <a href={props.href} target={target}>
            <Text alignment={props.alignment}
                function={TextFunction.Link}>
                { props.children }
            </Text>
        </a>
    )
}

export default Link;
