import Text, { TextType } from '../../components/Text';

const Header = () => {
    return (
        <nav class="p-6 w-full">
            <div class="mx-2 flex flex-row md:justify-start justify-center">
                <Text type={TextType.Logo}>
                    GrammarGrove
                </Text>
            </div>
        </nav>
    );
}

export default Header;
