import Text, { TextType, TextAlignment } from '../../components/Text';

const Header = () => {
    return (
        <nav class="p-6 w-full">
            <Text type={TextType.Subtitle} alignment={TextAlignment.Left}>
                Grammar Grove
            </Text>
        </nav>
    );
}

export default Header;
