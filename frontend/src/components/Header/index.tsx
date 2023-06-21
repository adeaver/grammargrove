import Text, { TextType, TextAlignment } from '../../components/Text';

const Header = () => {
    return (
        <nav class="p-6 w-full">
            <Text type={TextType.Logo} alignment={TextAlignment.Left}>
                GrammarGrove
            </Text>
        </nav>
    );
}

export default Header;
