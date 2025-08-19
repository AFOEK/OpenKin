import React, { useMemo, useState } from "react";
import ReactDOM from "react-dom/client";
import App from "./App.jsx";
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { ThemeProvider, CssBaseline, IconButton, Box } from '@mui/material';
import { Sun, Moon } from "lucide-react";
import { makeTheme } from "./theme";
import AuthProvider from './auth/AuthContext.jsx';
import Landing from "./pages/Landing.jsx";

function Root(){
    const [mode, setMode] = useState(localStorage.getItem('color_mode') || 'light')
    const theme = useMemo(() => makeTheme(mode), [mode]);
    const toggle = () => {
        const next = mode === "light" ? "dark":"light"
        setMode(next)
        localStorage.setItem("color_mode", next)
    };

    const router = createBrowserRouter([
        {path: '/', element: <Landing />},
        {path: '/app/*', element: <App colorMode={mode} toggleColorMode={toggle}/>}
    ])

    return(
        <ThemeProvider theme={theme}>
            <CssBaseline />
            <AuthProvider>
                <RouterProvider router={router} />
                <Box sx={{position: "fixed", right: 16, bottom: 16, zIndex: 1300}}>
                    <IconButton
                        color="primary"
                        size="large"
                        onClick={toggle}
                        sx={{bgcolor:"background.paper", boxShadow:2}}
                        aria-label="toggle theme">
                        {mode === "light" ? <Moon size={18}/> : <Sun size={18}/>}
                    </IconButton>
                </Box>
            </AuthProvider>
        </ThemeProvider>
    )
}

ReactDOM.createRoot(document.getElementById('root')).render(<Root/>)