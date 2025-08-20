import { createContext, useContext, useEffect, useState } from "react";
import api, {setTokens, clearTokens} from '../api/client';

const AuthCtx = createContext(null);
export const useAuth = () => useContext(AuthCtx);

export default function AuthProvider({ children }){
    const [user, setUser] = useState(null);
    const [ready, setReady] = useState(false);

    async function login( {login, password} ) {
        const { data } = await api.post('/users/login', {email: login, username: login, password});
        setTokens({ access: data.access_token, refresh:data.refresh_token })

        const me = await api.get('/users/me');
        setUser(me.data);
    }

    function logout(){
        clearTokens();
        setUser(null);
        window.location.href = '/login';
    }

    useEffect(() => {
        (async () => {
            const token = localStorage.getItem('access_token');
            if(!token) return;
            try{
                const me = await api.get('/users/me');
                setUser(me.data);
            }catch {

            } finally{
                setReady(true);
            }
        })();
    }, []);

    return(
        <AuthCtx.Provider value={{user, ready, login, logout}}>
            {children}
        </AuthCtx.Provider>
    );
}