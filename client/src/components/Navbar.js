import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';
import ArrowBackIosNewIcon from '@mui/icons-material/ArrowBackIosNew';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

export default function Navbar({ cycle, setCycle, lastCycle, data, setData }) {
	const navigate = useNavigate();
	return (
		<Box sx={{ flexGrow: 1 }}>
			<AppBar position='static'>
				<Toolbar>
					<Typography
						variant='h6'
						component='div'
						onClick={() => navigate('/')}
					>
						Tomasulo Simulator
					</Typography>

					<Box sx={{ flexGrow: 1 }} />

					<Button
						color='inherit'
						onClick={() => {
							setCycle((cycle) => cycle - 1);
						}}
						disabled={cycle === 0}
					>
						<ArrowBackIosNewIcon />
					</Button>

					<Typography variant='h6' component='div'>
						Current Cycle: {cycle}
					</Typography>

					<Button
						color='inherit'
						onClick={async () => {
							await axios
								.get('http://127.0.0.1:5000/api/v1/tick')
								.then((response) => {
									setData((data) => [...data, response.data]);
									setCycle((cycle) => cycle + 1);
								})
								.catch((error) => {
									console.log(error);
								});
						}}
						disabled={cycle === lastCycle}
					>
						<ArrowForwardIosIcon />
					</Button>
				</Toolbar>
			</AppBar>
		</Box>
	);
}
