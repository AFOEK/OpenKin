import { useState } from "react";
import { Routes, Route, useParams, useNavigate, Link } from 'react-router-dom';
import { useAuth } from './auth/AuthContext';
import RequireAuth from './auth/RequireAuth';
import api from './api/client';
import { AppBar, Toolbar, Button, Container, TextField, Typography, Box, Stack, Paper } from '@mui/material';

function LoginPage(){
    const {login} = useAuth()
    const [loginField, setloginField] = useState('')
    const [password, setPassword] = useState('')
    const [err, setErr] = useState('')
    const nav = useNavigate()

    async function onSubmit(e){
        e.preventDefault()
        setErr('')
        try{
            await login({ login: loginField, password })
            nav('/')
        } catch (e){
            setErr('Invalid Credential !')
        }
    }

    return (
        <Container maxWidth="xs" sx={{ mt:8 }}>
            <Paper sx = {{ p: 3 }}>
                <Typography variant="h5" gutterBottom>Sign in</Typography>
                <Box component="form" onSubmit={onSubmit}>
                    <Stack spacing={2}>
                        <TextField label="Email or username" value={loginField} onChange={e=>setloginField(e.target.value)} placeholder="Username" fullWidth autoFocus />
                        <TextField label="Password" type="password" value={password} onChange={e=>setPassword(e.target.value)} fullWidth placeholder="Password" />
                        {err && <Typography color="error">{err}</Typography>}
                        <Button variant="contained" type="submit">Login</Button>
                    </Stack>
                </Box>
            </Paper>
        </Container>
    )
}

function NavBar(){
    const { user, logout } = useAuth()
    return (
        <AppBar position="static">
            <Toolbar sx={{ gap: 2 }}>
                <Button color="inherit" component={Link} to="/">Dashboard</Button>
                <Button color="inherit" component={Link} to={`/tree/${user?.id}`}>Family Tree</Button>
                <Button color="inherit" component={Link} to="/add-person">Add Person</Button>
                <Button color="inherit" component={Link} to="/add-relationship">Add Relationship</Button>
                <Box sx={{ flex:1 }} />
                <Button color="inherit" onClick={onToggleTheme}>{mode === 'light' ? 'Dark':'Light'}</Button>
                <Typography>{user?.username || user?.email}</Typography>
                <Button color="inherit" onClick={logout}>Logout</Button>
            </Toolbar>
        </AppBar>
    )
}

function Dashboard(){
    const { user } = useAuth()
    return(
        <Container>
            <Typography variant="h5">Welcome, {user?.username || user?.email}</Typography>
            <Typography sx={{ mt:1, color:'text.secondary' }}>
                Next: Try add person, add relationship, or Open "My Tree"
            </Typography>
        </Container>
    )
}

function TreeViewer(){
    const { personId } = useParams()
    const token = localStorage.getItem('access_token')
    const [rows, setRows] = useState([])

    async function load(){
        const res = await api.get(`/tree/tree/${personId}`, {
            headers: {Authorization: `Bearer ${token}`}
        })
        setRows(res.data)
    }
    useState(() => {load() }, [])

    return(
        <Container>
            <Typography variant="h6">Tree for {personId}</Typography>
            <pre style={{ background:'#111', color:'#0f0', padding:12, borderRadius:8 }}>
                {JSON.stringify(rows, null, 2)}
            </pre>
        </Container>
    )
}

function AddPerson() {
  const token = localStorage.getItem('access_token')
  const [form, setForm] = useState({
    latin_name:'', chinese_name:'', gender:0, dob:'', pob:'', dialect:'Cantonese', visibility:'family'
  })
  const [msg, setMsg] = useState('')

  async function submit(e) {
    e.preventDefault()
    setMsg('')
    try {
      const { data } = await api.post('/persons/', form, {
        headers: { Authorization: `Bearer ${token}` }
      })
      setMsg(`Created person: ${data.id}`)
    } catch {
      setMsg('Failed to create person')
    }
  }

  return (
    <Container maxWidth="sm" sx={{ mt: 3 }}>
      <Typography variant="h6">Add Person</Typography>
      <Box component="form" onSubmit={submit} sx={{ mt: 2 }}>
        <Stack spacing={2}>
          <TextField label="Latin name" value={form.latin_name}
            onChange={e=>setForm({...form, latin_name:e.target.value})} />
          <TextField label="Chinese name" value={form.chinese_name}
            onChange={e=>setForm({...form, chinese_name:e.target.value})} />
          <TextField label="Gender (0 male, 1 female)" type="number" value={form.gender}
            onChange={e=>setForm({...form, gender:Number(e.target.value)})} />
          <TextField label="DOB" type="date" value={form.dob} InputLabelProps={{ shrink: true }}
            onChange={e=>setForm({...form, dob:e.target.value})} />
          <TextField label="Place of birth" value={form.pob}
            onChange={e=>setForm({...form, pob:e.target.value})} />
          <TextField label="Dialect" value={form.dialect}
            onChange={e=>setForm({...form, dialect:e.target.value})} />
          <TextField label="Visibility" value={form.visibility}
            onChange={e=>setForm({...form, visibility:e.target.value})} />
          <Button variant="contained" type="submit">Save</Button>
          {msg && <Typography>{msg}</Typography>}
        </Stack>
      </Box>
    </Container>
  )
}

function AddRelationship() {
  const token = localStorage.getItem('access_token')
  const [form, setForm] = useState({
    from_person_name:'', to_person_name:'', relationship_type:'sibling',
    visibility:'family', is_adopted:false, confidence:100, notes:''
  })
  const [msg, setMsg] = useState('')

  async function submit(e) {
    e.preventDefault()
    setMsg('')
    try {
      const { data } = await api.post('/relationships/', form, {
        headers: { Authorization: `Bearer ${token}` }
      })
      setMsg(`Created relationship: ${data.id}`)
    } catch {
      setMsg('Failed to create relationship')
    }
  }

  return (
    <Container maxWidth="sm" sx={{ mt: 3 }}>
      <Typography variant="h6">Add Relationship</Typography>
      <Box component="form" onSubmit={submit} sx={{ mt: 2 }}>
        <Stack spacing={2}>
          <TextField label="From (Latin or Chinese)" value={form.from_person_name}
            onChange={e=>setForm({...form, from_person_name:e.target.value})} />
          <TextField label="To (Latin or Chinese)" value={form.to_person_name}
            onChange={e=>setForm({...form, to_person_name:e.target.value})} />
          <TextField label="Type (e.g., sibling/parent/child/spouse/cousin)"
            value={form.relationship_type}
            onChange={e=>setForm({...form, relationship_type:e.target.value})} />
          <TextField label="Visibility" value={form.visibility}
            onChange={e=>setForm({...form, visibility:e.target.value})} />
          <TextField label="Confidence (0-100)" type="number" value={form.confidence}
            onChange={e=>setForm({...form, confidence:Number(e.target.value)})} />
          <TextField label="Notes" value={form.notes}
            onChange={e=>setForm({...form, notes:e.target.value})} />
          <Button variant="contained" type="submit">Save</Button>
          {msg && <Typography>{msg}</Typography>}
        </Stack>
      </Box>
    </Container>
  )
}

export default function App({colorMode, toggleColorMode}) {
  const { user } = useAuth()
  return (
    <>
      {user && <NavBar onToggleTheme={toggleColorMode} mode={colorMode}/>}
      <Routes>
        <Route path="login" element={<LoginPage />} />
        <Route index element={<RequireAuth><Dashboard /></RequireAuth>} />
        <Route path="tree/:personId" element={<RequireAuth><TreeViewer /></RequireAuth>} />
        <Route path="add-person" element={<RequireAuth><AddPerson /></RequireAuth>} />
        <Route path="add-relationship" element={<RequireAuth><AddRelationship /></RequireAuth>} />
      </Routes>
    </>
  )
}