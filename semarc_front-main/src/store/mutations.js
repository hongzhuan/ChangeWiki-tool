import { removeToken, setToken } from "@/js/storage";

export default {
    setToken(state, token) {
        state.token = token;
        setToken(token);
    },
    removeToken(state) {
        state.token = null;
        removeToken();
    }
}