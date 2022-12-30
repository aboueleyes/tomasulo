import BasicTable from '../components/BasicTable';
import styled from 'styled-components';
import Navbar from '../components/Navbar';
import BasicTabs from '../components/Tabs';
import { Grid, Typography } from '@mui/material';
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

const Simulation = () => {
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
		<>
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
		</>
	);
};

export default Simulation;
