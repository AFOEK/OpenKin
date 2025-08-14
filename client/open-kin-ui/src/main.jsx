import React from "react";
import ReactDOM from "react-dom/client"
import App from "./App.jsx"
import { BrowserRouter } from 'react-router-dom'
import { ThemeProvider, CssBaseline, createTheme } from '@mui/material'
import AuthProvider from './auth/AuthContext.jsx'

const theme = createTheme({
    palette: {mode: 'light'}
})

ReactDOM.createRoot(document.getElementById('root')).render(
    <React.StrictMode>
        <ThemeProvider theme={theme}>
            <CssBaseline />
            <AuthProvider>
                <BrowserRouter>
                <App />
                </BrowserRouter>
            </AuthProvider>
        </ThemeProvider>
    </React.StrictMode>
)