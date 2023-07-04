import { makeGetRequest } from '../../../util/gfetch';

export type AvailablePlan = {
    external_price_ref: string;
    price_cents_usd: number;
    interval: string;
    price_per_year_usd: number | null;
}

export type SubscriptionStatus = {
    available_plans: Array<AvailablePlan> | null;
    management_url: string | null;
}

export function getSubscriptionStatus(
    onSuccess: (resp: SubscriptionStatus) => void,
    onError: (err: Error) => void
) {
    makeGetRequest(
        "/api/billing/v1/status/?format=json",
        onSuccess,
        onError
    );
}
