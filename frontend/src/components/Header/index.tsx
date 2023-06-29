import Text, { TextType, TextAlignment } from '../../components/Text';

const Header = () => {
    return (
        <nav class="p-6 w-full">
            <div class="mx-2">
                <Text type={TextType.Logo} alignment={TextAlignment.Left}>
                    GrammarGrove
                </Text>
            </div>
        </nav>
    );
}

export default Header;
