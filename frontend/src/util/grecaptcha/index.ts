declare const window: any;

const SITE_KEY = '6Ledn2InAAAAAOl-IfKo27muly4vOOSceu5B8rOC';

export const withCaptchaToken = (actionName: string, fn: (token: string) => void) => {
    window.grecaptcha.ready(() => {
        window.grecaptcha.execute(SITE_KEY, { action: actionName })
        .then((token: string) => {
            fn(token);
        });
    });
}

export const loadCaptchaScript = () => {
    const script = document.createElement("script")
    script.src = `https://www.google.com/recaptcha/api.js?render=${SITE_KEY}`
    document.body.appendChild(script)
}
