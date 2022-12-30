import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';
import ArrowBackIosNewIcon from '@mui/icons-material/ArrowBackIosNew';

export default function Navbar({ cycle, setCycle, lastCycle }) {
	return (
		<Box sx={{ flexGrow: 1 }}>
			<AppBar position='static'>
				<Toolbar>
					<Typography variant='h6' component='div'>
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
						onClick={() => {
							setCycle((cycle) => cycle + 1);
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
