import React, { useMemo, useState } from "react";
import ReactDOM from "react-dom/client"
import App from "./App.jsx"
import { BrowserRouter } from 'react-router-dom'
import { ThemeProvider, CssBaseline, createTheme } from '@mui/material'
import AuthProvider from './auth/AuthContext.jsx'

function Root(){
    const [mode, setMode] = useState(localStorage.getItem('color_mode') || 'light')
    const theme = useMemo(() => createTheme({ palette: {mode} }), [mode])
    const toggleMode = () => {
        const next = mode === 'light' ? 'dark':'light'
        setMode(next)
        localStorage.setItem('color_mode', next)
    }
    return(
        <ThemeProvider theme={theme}>
            <CssBaseline />
            <AuthProvider>
                <BrowserRouter>
                <App colorMode={mode} toggleColorMode={toggleMode}/>
                </BrowserRouter>
            </AuthProvider>
        </ThemeProvider>
    )
}

ReactDOM.createRoot(document.getElementById('root')).render(<Root/>)