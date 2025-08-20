import {createTheme} from "@mui/material/styles";

const common = {
    shape: {borderRadius: 14},
    typography:{
        fontFamily: "Inter, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif",
        h1: { fontWeight: 800, letterSpacing: -0.5 },
        h2: { fontWeight: 700, letterSpacing: -0.4 },
        h3: { fontWeight: 700, letterSpacing: -0.3 },
    },
    components:{
        MuiPaper:{
            styleOverrides:{
                rounded: {borderRadius: 14},
                elevation1: {boxShadow: "0px 6px 20px rgba(0,0,0,0.06)"}
            }
        },
        MuiButton:{
            defaultProps:{disableElevation: true},
            styleOverrides:{
                root: {borderRadius: 12, textTransform:"none", fontWeight:600}
            }
        },
        MuiAppBar:{
            defaultProps: { elevation: 0, color: "transparent" },
            styleOverrides:{
                root:({theme}) => ({
                    backdropFilter: "saturate(120%) blur(6px)",
                    backgroundColor: "transparent",
                    color: theme.palette.text.primary,
                    borderBottom: `1px solid ${theme.palette.divider}`
                })
            }
        }
    }
};

const pastelLight = {
    mode: "light",
    primary: {main: "#7C8CF8"},
    secondary: {main: "#F59DCB"},
    success: {main: "#81D8AE"},
    info: {main: "#8BD3E6"},
    warning: {main: "#F8D477"},
    error: {main: "#C23B22"},
    background: {default: "#FAFBFF", paper: "#FFFFFF"}
};

const pastelDark = {
    mode: "dark",
    primary: {main: "#9DA7FB"},
    secondary: {main: "#F5B3D7"},
    success: {main: "#96E1BE"},
    info: {main: "#A3E0EE"},
    warning: {main: "#FADC8E"},
    error: {main: "#C0432DFF"},
    background: { default: "#0C0E12", paper: "#12141A" }
};

export const makeTheme = (mode = "light") =>
    createTheme({
        palette: mode === "light" ? pastelLight : pastelDark,
        ...common
    });