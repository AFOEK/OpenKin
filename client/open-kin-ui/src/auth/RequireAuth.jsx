import { Navigate, Outlet } from 'react-router-dom';
import { Box, CircularProgress } from '@mui/material';
import { useAuth } from './AuthContext';

export default function RequireAuth({ children }){
    const {user, ready} = useAuth();
    if(!ready){
        return (
            <Box sx={{ minHeight: '40vh', display: 'grid', placeItems: 'center' }}>
                <CircularProgress/>
            </Box>
        )
    }
    if(!user) return <Navigate to="/login" replace />
    return children ?? <Outlet/>;
}