import './App.css';
import BasicTable from './components/BasicTable';
import styled from 'styled-components';
import Navbar from './components/Navbar';
import BasicTabs from './components/Tabs';
import { Box, Grid, Typography } from '@mui/material';
import { useEffect, useState } from 'react';
import axios from 'axios';

const HorizontalContainer = styled.div`
	display: flex;
	flex-direction: row;
	height: 100vh;
	background-color: #f5f5f5;
`;

const LeftSideContainer = styled.div`
	display: flex;
	flex-direction: column;
	width: 450px;
	height: 100vh;
	background-color: #f5f5f5;
`;

const MainContainer = styled.div`
	display: flex;
	flex-direction: column;
	height: 100vh;
	background-color: #f5f5f5;
	margin: 20px;
`;

function App() {
	const [data, setData] = useState(null);
	const [cycle, setCycle] = useState(0);

	useEffect(() => {
		const fetchData = async () => {
			const result = await axios.get('http://localhost:3001/data');
			return result.data;
		};

		fetchData()
			.then((data) => {
				setData(data);
			})
			.catch((err) => {
				console.log(err);
			});
	}, []);

	if (!data) return <div>Loading...</div>;

	return (
		<div className='App'>
			<Navbar lastCycle={data.length - 1} cycle={cycle} setCycle={setCycle} />
			<HorizontalContainer>
				<LeftSideContainer>
					<BasicTabs
						tabNames={['Register File', 'Memory']}
						components={[
							<BasicTable content={data[cycle].registers} />,
							<BasicTable content={data[cycle].memory} />,
						]}
					/>
				</LeftSideContainer>

				<MainContainer>
					<Grid container spacing={2}>
						<Grid item md={6} lg={6}>
							<Typography variant='h6'>
								{'Addition Reservation Stations'}
							</Typography>
							<BasicTable content={data[cycle].reservation.A} />
						</Grid>

						<Grid item md={6} lg={6}>
							<Typography variant='h6'>
								{'Multiplication Reservation Stations'}
							</Typography>
							<BasicTable content={data[cycle].reservation.M} />
						</Grid>

						<Grid item md={6} lg={6}>
							<Typography variant='h6'>
								{'Load Reservation Stations'}
							</Typography>
							<BasicTable content={data[cycle].buffer.L} />
						</Grid>

						<Grid item md={6} lg={6}>
							<Typography variant='h6'>
								{'Store Reservation Stations'}
							</Typography>
							<BasicTable content={data[cycle].buffer.S} />
						</Grid>
					</Grid>
				</MainContainer>
			</HorizontalContainer>
		</div>
	);
}

const data = {
	buffer: {
		L: {
			L1: {
				tag: 'L1',
				busy: false,
				address: 0,
				time: 0,
				state: 'writing back',
			},
			L2: {
				tag: 'L2',
				busy: false,
				address: null,
				time: -1,
				state: 'issued',
			},
			L3: {
				tag: 'L3',
				busy: false,
				address: null,
				time: -1,
				state: 'issued',
			},
		},
		S: {
			S1: {
				tag: 'S1',
				busy: false,
				address: 1,
				v: 2.0,
				q: null,
				time: 0,
				state: 'writing back',
			},
			S2: {
				tag: 'S2',
				busy: false,
				address: null,
				v: null,
				q: null,
				time: -1,
				state: 'issued',
			},
			S3: {
				tag: 'S3',
				busy: false,
				address: null,
				v: null,
				q: null,
				time: -1,
				state: 'issued',
			},
		},
	},
	reservation: {
		A: {
			A1: {
				tag: 'A1',
				busy: false,
				op: 'ADD.D',
				vj: 1.0,
				vk: 1.0,
				qj: null,
				qk: null,
				time: 0,
				state: 'writing back',
			},
			A2: {
				tag: 'A2',
				busy: false,
				op: null,
				vj: null,
				vk: null,
				qj: null,
				qk: null,
				time: -1,
				state: 'issued',
			},
			A3: {
				tag: 'A3',
				busy: false,
				op: null,
				vj: null,
				vk: null,
				qj: null,
				qk: null,
				time: -1,
				state: 'issued',
			},
		},
		M: {
			M1: {
				tag: 'M1',
				busy: false,
				op: null,
				vj: null,
				vk: null,
				qj: null,
				qk: null,
				time: -1,
				state: 'issued',
			},
			M2: {
				tag: 'M2',
				busy: false,
				op: null,
				vj: null,
				vk: null,
				qj: null,
				qk: null,
				time: -1,
				state: 'issued',
			},
		},
	},
	memory: {
		0: {
			address: 0,
			value: 1.0,
		},
		1: {
			address: 1,
			value: 2.0,
		},
		2: {
			address: 2,
			value: 3.0,
		},
	},
	registers: {
		R0: {
			Register: 'R0',
			Value: 0,
		},
		R1: {
			Register: 'R1',
			Value: 1,
		},
		R2: {
			Register: 'R2',
			Value: 2,
		},
	},
	cycle: 9,
};

export default App;
