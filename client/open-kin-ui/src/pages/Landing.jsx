import * as React from 'react';
import { AppBar, Toolbar, Button, Container, Box, Typography, Paper } from '@mui/material';
import App from '../App';
import GoalsSection from "../components/GoalsSections";

const Section = ({id, title, subtitle, children}) => (
    <Box id={id}
    component="section"
    sx={{
        scrollSnapAlign:'start',
        minHeight: '100vh',
        display: 'grid',
        alignContent: 'center',
        py:8
    }}
    >
        <Container maxWidth="lg" sx={{ textAlign:'center' }}>
            <Typography variant='h2' gutterBottom>{title}</Typography>
            {subtitle && <Typography color='text.secondary' sx={{ mb: 4 }}>{subtitle}</Typography>}
            {children}
        </Container>
    </Box>
)

export default function Landing(){
    return(
        <>
        <AppBar position='fixed' color='transparent' elevation={0} sx={{backdropFilter: 'saturate(120%) blur(6px)'}}>
            <Toolbar>
                <Typography variant='h6' sx={{ flexGrow: 1 }}>OpenKin</Typography>
                <Button href='#feature' sx={{ mr: 1}}>Features</Button>
                <Button href='#privacy' sx={{mr: 1}}>Privacy</Button>
                <Button href='#goals' sx={{mr: 1}}>Goals</Button>
                {/* <Button href='#statistic' sx={{mr: 1}}>Statistic</Button> */}
                <Button href='#cta' variant='contained'>Get Started</Button>
            </Toolbar>
        </AppBar>
        <Box
            sx={{
                scrollSnapType:'y mandatory',
                overflow:'auto',
                height:'100vh'
            }}
        >
            <Section
                id="hero"
                title="Preserve Your Family Story"
                subtitle="Add people, connect relationships, and keep media in one secure place."
            >
                <Box sx={{display:'flex', justifyContent:'center', gap:2}}>
                    <Button size='large' variant='contained' href='/app'>Get Started</Button>
                    <Button size='large' href='#feature'>Learn More</Button>
                </Box>
            </Section>

            <Section id="feature" title="Everything in One Place">
                <Box sx={{
                    display: 'grid',
                    gap: 2,
                    gridTemplateColumns: {xs: '1fr', md: '1fr 1fr 1fr'}
                }}>
                    {[
                        {t:'People & Relations', b: 'Create persons and link parent/child, spouse, sibling.'},
                        {t:'Media Library', b: 'Attach photos and documents to people and events.'},
                        {t:'Privacy Control', b: 'Granular visibility: public, family, clan, private'},
                    ].map(card => (
                        <Paper key={card.t} sx={{p:3}}>
                            <Typography variant="h6">{card.t}</Typography>
                            <Typography color="text.secondary" sx={{mt: 1}}>{card.b}</Typography>
                        </Paper>
                    ))}
                </Box>
            </Section>

            <Section id="privacy" title="Built with Privacy in Mind">
                <Typography sx={{maxWidth: 760, mx:"auto"}}>
                    Role-based access, per-record visibility, and export controls give you confidence
                    that sensitive history stays within your circle.
                </Typography>
            </Section>

            <GoalsSection />

            {/* <StatsSection /> */}
            <Section id="cta" title="Ready to Start ?">
                <Button size="large" variant='contained' href="/app">Get Started</Button>
            </Section>
        </Box>
        </>
    )
}