import BasicTable from '../components/BasicTable';
import styled from 'styled-components';
import Navbar from '../components/Navbar';
import { Grid, Typography } from '@mui/material';
import { useState } from 'react';
import { useLocation } from 'react-router';
import SideTabs from '../components/SideTabs';

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
	const location = useLocation();
	const [cycle, setCycle] = useState(0);
	const [data, setData] = useState([location.state]);

	return (
		<>
			<Navbar
				lastCycle={10}
				cycle={cycle}
				setCycle={setCycle}
				data={data}
				setData={setData}
			/>
			<HorizontalContainer>
				<LeftSideContainer>
					{/* <BasicTabs
						tabNames={['Register File', 'Memory']}
						components={[
							<BasicTable content={data[cycle].registers} />,
							<BasicTable content={data[cycle].memory} />,
						]}
					/> */}
					<SideTabs
						registers={data[cycle].registers}
						memory={data[cycle].memory}
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
