import Text from '../../components/Text';
import RadioButton from '../../components/RadioButton';

type Option = {
    hskLevel: number;
    text: string;
}

const options: Option[] = [
    { hskLevel: 0, text: "Just starting out (Not quite HSK 1)" },
    { hskLevel: 1, text: "Beginner (HSK 1)" },
    { hskLevel: 2, text: "Lower Intermediate (HSK 2)" },
    { hskLevel: 3, text: "Intermediate (HSK 3)" },
    { hskLevel: 4, text: "Upper Intermediate (HSK 4)" },
    { hskLevel: 5, text: "Lower Advanced (HSK 5)" },
    { hskLevel: 6, text: "Advanced (HSK 6)" },
]

type HSKLevelDisplayProps = {
    currentHSKLevel: number | null;
    setCurrentHSKLevel: (level: number) => void;
}

const HSKLevelDisplay = (props: HSKLevelDisplayProps) => {
    return (
        <div class="w-full">
        {
            options.map((o: Option) => (
                <div class="flex flex-row space-x-2" onClick={() => props.setCurrentHSKLevel(o.hskLevel)}>
                    <RadioButton isSelected={props.currentHSKLevel === o.hskLevel} />
                    <Text>
                        { o.text }
                    </Text>
                </div>
            ))
        }
        </div>
    );
}

export default HSKLevelDisplay;
