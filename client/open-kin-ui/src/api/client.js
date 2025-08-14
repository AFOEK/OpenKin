import axios from 'axios';

const api = axios.create({baseURL: import.meta.env.VITE_API_BASE});

let accessToken = localStorage.getItem('access_token')
let refreshToken = localStorage.getItem('refresh_token')

export function setTokens({access, refresh}){
    if (access){
        accessToken = access;
        localStorage.setItem('access_token', access)
    }
    if(refresh){
        refreshToken = refresh
        localStorage.setItem('refresh_token', refresh)
    }
}

export function clearToken(){
    accessToken = null;
    refreshToken = null;
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
}

api.interceptors.request.use((config) => {
    if (accessToken){
        config.headers.Authorization = `Bearer ${accessToken}`;
        return config;
    }
});

api.interceptors.response.use(
    r => r,
    async(error) => {
        const original = error.config;
        if(error.response?.status === 401 && !original._retry && refreshToken){
            if (refreshing){
                return new Promise((resolve, reject) => queue.push({resolve, reject}));
            }
            original._retry = true;
            refresh = true;

            try{
                const res = await axios.post(
                    `${import.meta.env.VITE_API_BASE/users/refresh}`,
                    {},
                    {headers: {Authorization: `Bearer ${refreshToken}`}}
                );
                setTokens({ access: res.data.access_token });
                queue.forEach(p => p.resolve(api(original)));
                queue = [];
                return api(original);
            } catch (e){
                queue.forEach(p => p.reject(e));
                queue = [];
                clearToken();
                window.location.href = '/login';
                return Promise.reject(e);
            } finally {
                refreshing = false
            }
        }
    }
);

export default api;