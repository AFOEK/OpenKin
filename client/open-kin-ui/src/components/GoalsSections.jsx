import * as React from "react";
import { Box, Container, Typography, Grid, Paper } from "@mui/material";
import { Target, Globe, Shield, Users } from "lucide-react";

const goals = [
    {
        icon: <Target size={28} />,
        title: "Preserve family heritage",
        body: "Capture and safeguard Chinese diaspora family history across generations."
    },
    {
        icon: <Globe size={28} />,
        title: "Multi-language Support",
        body: "Enable records in multiple scripts and dialects, reflecting cultural diversity."
    },
    {
        icon: <Shield size={28} />,
        title: "Secure & Private",
        body: "Role-based access ensure sensitve information stays within the right circle."
    },
    {
        icon: <Users size={28} />,
        title: "Community Collaboration",
        body: "Allow relative to contribute stories, media, and relationships together."
    }
]

export default function GoalsSection(){
    return(
        <Box
        id="goals"
        component="section"
        sx={{
            scrollSnapAlign: "start",
            minHeight:"100vh",
            display:"grid",
            alignContent:"center",
            py:8,
            bgcolor:"background.default"
        }}
        >
            <Container maxWidth="lg">
                <Typography variant="h3" align="center" gutterBottom>
                    Our Goals
                </Typography>
                <Typography align="center" color="text.secondary" sx={{ mb:6, maxWidth:720, mx:"auto" }}>
                    OpenKin is guided by clear gaols to ensure family stories are preserved, accessible,
                    and meaningful for generation to come.
                </Typography>
                <Grid 
                container 
                spacing={3}
                sx={{maxWidth: 1100,
                    mx:"auto"
                }}>
                    {goals.map((g)=> (
                        <Grid item xs={12} md={6} sm={6} key={g.title}>
                            <Paper sx={{
                                p:4,
                                display:"flex",
                                flexDirection:"column",
                                alignItems:"flex-start",
                                gap:1.5,
                                height:"100%",
                                transition:"transform 0.2s, box-shadow 0.2s",
                                "&:hover": {transform: "translateY(-4px)", boxShadow:6}
                            }}>
                                <Box
                                sx={{
                                    width:48,
                                    height:48,
                                    borderRadius: "50%",
                                    bgcolor:"primary.main",
                                    color:"primary.contrastText",
                                    display:"flex",
                                    alignItems:"center",
                                    justifyContent:"center",
                                    mb: 1
                                }}>
                                    {g.icon}
                                </Box>
                                <Typography variant="h6">{g.title}</Typography>
                                <Typography color="text.secondary" sx={{mt: 0.5}}>{g.body}</Typography>
                            </Paper>
                        </Grid>
                    ))}
                </Grid>
            </Container>
        </Box>
    )
}