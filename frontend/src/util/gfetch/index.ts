function getCookie(name: string): string | null {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

export function getCSRFToken(): string | null {
    return getCookie("csrftoken");
}

export function makePostRequest<T, U>(
    url: string,
    body: T,
    onSuccess: (resp: U) => void,
    onError: (e: Error) => void,
) {
    fetch(url, {
        credentials: 'include',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'cache': 'no-cache',
            'X-CSRFToken': getCSRFToken() || "",
        },
        body: JSON.stringify(body),
    })
    .then(response => {
        if (!response.ok) {
            response.text().then(data => onError(new Error(data)));
            return
        }
        response.json().then(data => onSuccess(data as U));
    })
    .catch(onError);
}
