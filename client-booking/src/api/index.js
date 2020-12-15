/* eslint-disable no-restricted-globals */

// get param direct from process.env, because of bundle param
export const API_BASE =
    process.env.REACT_APP_API_BASE || window.location.origin;

export const WS_BASE = API_BASE.replace(/^http/, 'ws');

export const rejectErrors = (res) => {
    const { status } = res;
    if (status === 400) {
        window.location.href = '/login';
        return;
    }
    if (status >= 200 && status < 300) {
        return res.json();
    }
    // we can get message from Promise but no need, just use statusText instead of
    // server return errors, also status code
    return Promise.reject({ message: res.statusText, status, res });
};
// try invoke callback for refresh token here
export const fetchWithOptions = (url, options = {}, base = API_BASE) => {
    // in the same server, API_BASE is emtpy
    // check convenient way of passing base directly
    return (
        fetch(/^(?:https?)?:\/\//.test(url) ? url : base + url, options)
            .then(rejectErrors)
            // default return empty json when no content, we always use json, never use plain text
            .catch((ex) => console.log(ex))
    );
};


export const fetchJson = (url, options = {}, base = API_BASE) =>
    // in the same server, API_BASE is emtpy
    // check convenient way of passing base directly
    fetchWithOptions(
        url,
        {
            ...options,
            headers: {
                ...options.headers,
                Accept: 'application/json',
                'Content-Type': 'application/json'
            }
        },
        base
    );

// only post have post data
export const get = (url, { method = 'GET', signal = null, token } = {}) =>
    fetchJson(url, {
        method,
        headers: {
            Authorization: token || localStorage.getItem('authorization')
        },
        signal
    });

export const post = (url, { data, signal = null, token } = {}) =>
    fetchJson(url, {
        method: 'POST',
        headers: {
            Authorization: token || localStorage.getItem('authorization')
        },
        signal,
        body: JSON.stringify(data)
    });