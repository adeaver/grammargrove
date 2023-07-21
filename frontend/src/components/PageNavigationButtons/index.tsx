import Button, { ButtonType } from '../../components/Button';

type PageNavigationButtonsProps = {
    getNextPage?: () => void;
    getPreviousPage?: () => void;
}

const PageNavigationButtons = (props: PageNavigationButtonsProps) => {
    return (
        <div class="flex flex-row space-x-4">
            {
                !!props.getPreviousPage && (
                    <Button type={ButtonType.Secondary} onClick={props.getPreviousPage}>
                        Previous Page
                    </Button>
                )
            }
            {
                !!props.getNextPage && (
                    <Button type={ButtonType.Secondary} onClick={props.getNextPage}>
                        Next Page
                    </Button>
                )
            }
        </div>
    )
}

export default PageNavigationButtons;
