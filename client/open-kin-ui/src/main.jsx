import React, { useMemo, useState } from "react";
import ReactDOM from "react-dom/client"
import App from "./App.jsx"
import { createBrowserRouter, BrowserRouter, RouterProvider } from 'react-router-dom'
import { ThemeProvider, CssBaseline, createTheme } from '@mui/material'
import AuthProvider from './auth/AuthContext.jsx'
import Landing from "./pages/Landing.jsx";

function Root(){
    const [mode, setMode] = useState(localStorage.getItem('color_mode') || 'light')
    const theme = useMemo(() => createTheme({ palette: {mode} }), [mode])
    const toggleMode = () => {
        const next = mode === 'light' ? 'dark':'light'
        setMode(next)
        localStorage.setItem('color_mode', next)
    }

    const router = createBrowserRouter([
        {path: '/', element: <Landing />},
        {path: '/app/*', element: <App colorMode={mode} toggleColorMode={toggleMode}/>}
    ])

    return(
        <ThemeProvider theme={theme}>
            <CssBaseline />
            <AuthProvider>
                <RouterProvider router={router} />
            </AuthProvider>
        </ThemeProvider>
    )
}

ReactDOM.createRoot(document.getElementById('root')).render(<Root/>)