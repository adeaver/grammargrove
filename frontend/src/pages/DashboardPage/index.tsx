import {
    setLocation
} from '../../util/window';

import Header from '../../components/Header';
import Card from '../../components/Card';
import Text, { TextType, TextAlignment, TextFunction } from '../../components/Text';
// import LoadingIcon from '../../components/LoadingIcon';

const DashboardPage = () => {
    const pages: Array<PageLinkProps> = [
        { title: "Quiz", description: "Practice your vocabulary and grammar rules", url: "/quiz/" },
        { title: "Vocabulary", description: "Update your vocabulary words. You can add a new word you learned or remove a word.", url: "/vocabulary/" },
        { title: "Grammar", description: "Update your grammar rules. You can add a new rule you learned or remove one.", url: "/grammar/" },
        { title: "Preferences", description: "Update your preferences, such as email preferences or Mandarin level.", url: "/preferences/" },
    ]

    return (
        <div>
            <Header />
            <div class="grid grid-cols-2 gap-4">
            {
                pages.map((p: PageLinkProps, idx: number) => (
                    <PageLink key={`page-link-${idx}`} {...p} />
                ))
            }
            </div>
        </div>
    );
}

type PageLinkProps = {
    title: string;
    description: string;
    url: string;
}

const PageLink = (props: PageLinkProps) => {
    return (
        <div class="cursor-pointer col-span-2 md:col-span-1" onClick={() => setLocation(props.url)}>
            <Card className="flex flex-col space-y-2">
                <Text
                    type={TextType.Subtitle}
                    alignment={TextAlignment.Left}
                    function={TextFunction.Primary}>
                    { props.title }
                </Text>
                <hr />
                <Text alignment={TextAlignment.Left}>
                    { props.description }
                </Text>
            </Card>
        </div>
    )
}

export default DashboardPage;
