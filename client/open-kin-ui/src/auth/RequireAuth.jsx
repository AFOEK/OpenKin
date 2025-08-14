import {Navigate, useActionData} from 'react-router-dom';
import { useAuth } from './AuthContext';

export default function RequireAuth({ children }){
    const {user} = useAuth();
    if(!user) return <Navigate to="/login" replace />
    return children;
}