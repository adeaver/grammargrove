export enum TextType {
    Title = 'title',
    Subtitle = 'subtitle',
    SectionHeader = 'section-header',
    Body = 'body',
    FinePrint = 'fine-print'
}

export enum TextFunction {
    Primary = 'primary',
    Display = 'display',
    Confirmation = 'confirmation',
    Warning = 'warning',
}

export enum TextAlignment {
    Center = 'center',
    Left = 'left',
    Right = 'right',
}

export type TextProps = {
    children: string;
    type?: TextType;
    function?: TextFunction;
    alignment?: TextAlignment;
}

const getClassesForProps = (props: TextProps) => {
    let classes: string[] = [];
    switch (props.type) {
        case undefined:
        case null:
        case TextType.Body:
            classes = classes.concat(["text-lg", "font-body"]);
            break;
        case TextType.Title:
            classes = classes.concat(["text-4xl", "font-body", "font-bold"]);
            break;
        case TextType.Subtitle:
            classes = classes.concat(["text-2xl", "font-body", "font-bold"]);
            break;
        case TextType.SectionHeader:
            classes = classes.concat(["text-xl", "font-body"]);
            break;
        case TextType.FinePrint:
            classes = classes.concat(["text-md", "font-body"]);
            break;
        default:
            throw new Error(`Unexpected text type ${props.type}`);
    }
    switch (props.function) {
        case undefined:
        case null:
        case TextFunction.Display:
            classes = classes.concat(["text-text-700"]);
            break;
        case TextFunction.Primary:
            classes = classes.concat(["text-primary-600"]);
            break;
        case TextFunction.Confirmation:
            classes = classes.concat(["text-confirmation-600"]);
            break;
        case TextFunction.Warning:
            classes = classes.concat(["text-warning-500"]);
            break;
        default:
            throw new Error(`Unexpected function ${props.type}`);
    }
    switch (props.alignment) {
        case undefined:
        case null:
        case TextAlignment.Center:
            classes = classes.concat(["text-center"]);
            break;
        case TextAlignment.Left:
            classes = classes.concat(["text-left"]);
            break;
        case TextAlignment.Right:
            classes = classes.concat(["text-right"]);
            break;
    }
    return classes.join(" ");
}

const Text = (props: TextProps) => {
    const classes = getClassesForProps(props);
    switch (props.type) {
        case undefined:
        case null:
        case TextType.Body:
        case TextType.FinePrint:
            return <p className={classes}>{props.children}</p>
        case TextType.Title:
            return <h1 className={classes}>{props.children}</h1>
        case TextType.Subtitle:
            return <h2 className={classes}>{props.children}</h2>
        case TextType.SectionHeader:
            return <h3 className={classes}>{props.children}</h3>
    }
    throw new Error(`Unrecognized text type ${props.type}`);
}

export default Text;
