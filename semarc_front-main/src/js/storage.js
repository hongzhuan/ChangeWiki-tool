const ls = window.sessionStorage;
const TOKEN_KEY = '__token__'

//获取缓存数据
export const getStorageItem = (key) => {
    try {
        return JSON.parse(ls.getItem(key));
    } catch (err) {
        return '';
    }
}

//存储数据
export const setStorageItem = (key, val) => {
    ls.setItem(key, JSON.stringify(val));
}

//清楚缓存
export const clearStorage = () => {
    ls.clear();
}

//
export const keys = (index) => {
    return ls.key(index);
}

//删除缓存
export const removeStorageItem = (key) => {
    if (ls.getItem(key)) {
        ls.removeItem(key);
    }
}

export function setToken(token) {
    ls.setItem(TOKEN_KEY, token);
}

export function getToken() {
    return ls.getItem(TOKEN_KEY)
}

export function removeToken() {
    ls.removeItem(TOKEN_KEY)
}