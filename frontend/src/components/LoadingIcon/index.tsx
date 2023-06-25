import Text from '../../components/Text';

export enum LoadingIconSize {
    Large = 'large',
    Medium = 'medium',
    Small = 'small'
}

export enum LoadingIconColor {
    Primary = 'primary',
    Secondary = 'secondary'
}

type LoadingIconProps = {
    size?: LoadingIconSize;
    color?: LoadingIconColor;
}

const LoadingIcon = (props: LoadingIconProps) => {
    let size: string | null;
    if (!props.size || props.size === LoadingIconSize.Large) {
        size = '96';
    } else if (props.size === LoadingIconSize.Medium) {
        size = '48';
    } else if (props.size === LoadingIconSize.Small) {
        size = '24';
    } else {
        throw Error(`Unrecognized size ${props.size}`);
    }

    let color;
    if (!props.color || props.color === LoadingIconColor.Primary) {
        color = 'fill-primary-600';
    } else if (props.color === LoadingIconColor.Secondary) {
        color = 'fill-white';
    } else {
        throw Error(`Unrecognized color ${props.color}`);
    }

    return (
        <div class="w-full flex flex-col items-center space-y-4">
            <svg class={color} width={size} height={size} viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path d="M12,1A11,11,0,1,0,23,12,11,11,0,0,0,12,1Zm0,20a9,9,0,1,1,9-9A9,9,0,0,1,12,21Z" transform="translate(12, 12) scale(0)">
                    <animateTransform id="spinner_g88x" begin="0;spinner_yOmw.begin+0.6s" attributeName="transform" calcMode="spline" type="translate" dur="1.2s" values="12 12;0 0" keySplines=".52,.6,.25,.99"/>
                    <animateTransform begin="0;spinner_yOmw.begin+0.6s" attributeName="transform" calcMode="spline" additive="sum" type="scale" dur="1.2s" values="0;1" keySplines=".52,.6,.25,.99"/>
                    <animate begin="0;spinner_yOmw.begin+0.6s" attributeName="opacity" calcMode="spline" dur="1.2s" values="1;0" keySplines=".52,.6,.25,.99"/>
                </path>
                <path d="M12,1A11,11,0,1,0,23,12,11,11,0,0,0,12,1Zm0,20a9,9,0,1,1,9-9A9,9,0,0,1,12,21Z" transform="translate(12, 12) scale(0)">
                    <animateTransform id="spinner_yOmw" begin="spinner_g88x.begin+0.6s" attributeName="transform" calcMode="spline" type="translate" dur="1.2s" values="12 12;0 0" keySplines=".52,.6,.25,.99"/>
                    <animateTransform begin="spinner_g88x.begin+0.6s" attributeName="transform" calcMode="spline" additive="sum" type="scale" dur="1.2s" values="0;1" keySplines=".52,.6,.25,.99"/>
                    <animate begin="spinner_g88x.begin+0.6s" attributeName="opacity" calcMode="spline" dur="1.2s" values="1;0" keySplines=".52,.6,.25,.99"/>
                </path>
            </svg>
            <Text>
                Loading...
            </Text>
        </div>
    );
}

export default LoadingIcon;
