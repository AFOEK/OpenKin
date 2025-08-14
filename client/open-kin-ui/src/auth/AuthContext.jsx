import { createContext, useContext, useEffect, useState } from "react";
import api, {setToken, clearToken} from '../api/client';

const AuthCtx = createContext(null);
export const useAuth = () => useContext(AuthCtx);

export default function AuthProvider({ children }){
    const [user, setUser] = useState(null);

    async function login( {login, password} ) {
        const {data} = await api.post('/users.login', {email: login, username: login, password});
        localStorage.setItem('access_token', data.access_token);
        localStorage.setItem('refresh_token', data.refresh_token);

        const me = await api.get('/users/me', {
            headers: {Authorization: `Bearer $(data.access_token)`}
        });
        setUser(me.data);
    }

    function logout(){
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        setUser(null);
        window.location.href = '/login';
    }

    useEffect(() => {
        (async () => {
            const token = localStorage.getItem('access_token');
            if(!token) return;
            try{
                const me = await api.get('/users/me', {headers: {Authorization: `Bearer ${token}`}});
                setUser(me.data);
            }catch {

            }
        })();
    }, []);

    return(
        <AuthCtx.Provider value={{user, login, logout}}>
            {children}
        </AuthCtx.Provider>
    );
}