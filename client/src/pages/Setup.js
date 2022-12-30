import {
	DialogContent,
	DialogContentText,
	TextField,
	Typography,
} from '@mui/material';
import { useState } from 'react';
import FileEditor from '../components/FileEditor';
import styled from 'styled-components';
import LoadingButton from '@mui/lab/LoadingButton';
import * as Yup from 'yup';
import validateFormData from '../utils/validateFormData';
import axios from 'axios';
import { useNavigate } from 'react-router';

const HorizontalContainer = styled.div`
	display: flex;
	flex-direction: row;
	// height: 100vh;
	width: 100vw;
	margin: 20px;
`;

const Setup = () => {
	const navigate = useNavigate();

	const [code, setCode] = useState('');
	const [formData, setFormData] = useState({
		addLatency: 2,
		subLatency: 2,
		mulLatency: 4,
		divLatency: 4,
		loadLatency: 2,
		storeLatency: 2,
	});

	const [formErrors, setFormErrors] = useState(new Map());
	const [loading, setLoading] = useState(false);

	const validationRules = {
		addLatency: Yup.number().required().min(1).max(10),
		subLatency: Yup.number().required().min(1).max(10),
		mulLatency: Yup.number().required().min(1).max(10),
		divLatency: Yup.number().required().min(1).max(10),
		loadLatency: Yup.number().required().min(1).max(10),
		storeLatency: Yup.number().required().min(1).max(10),
	};

	const handleSubmit = () => {
		setLoading(true);
		setFormErrors(new Map());
		validateFormData(formData, validationRules)
			.then(async () => {
				const requestData = {
					instructions: code,
					latencies: {
						'ADD.D': formData.addLatency,
						'SUB.D': formData.subLatency,
						'MUL.D': formData.mulLatency,
						'DIV.D': formData.divLatency,
						'L.D': formData.loadLatency,
						'S.D': formData.storeLatency,
					},
				};

				await axios
					.post('http://127.0.0.1:5000/api/v1/run', requestData)
					.then((response) => {
						console.log(response.data);
						navigate('/run', { state: response.data });
					})
					.catch((error) => {
						console.log(error);
					});
			})
			.catch((errors) => {
				setFormErrors(errors);
			})
			.finally(() => {
				setLoading(false);
			});
	};

	return (
		<>
			<HorizontalContainer>
				<div>
					<Typography variant='h4' component='div'>
						Program
					</Typography>
					<FileEditor code={code} setCode={setCode} />
				</div>
				<DialogContent>
					<DialogContentText>Configuration</DialogContentText>

					<TextField
						required
						autoFocus
						margin='dense'
						id='addLatency'
						label='Add Instruction Latency'
						type='number'
						fullWidth
						variant='outlined'
						value={formData.addLatency}
						onChange={(e) =>
							setFormData({ ...formData, addLatency: e.target.value })
						}
						error={formErrors.has('addLatency')}
						helperText={formErrors.get('addLatency')}
					/>

					<TextField
						required
						autoFocus
						margin='dense'
						id='subLatency'
						label='Sub Instruction Latency'
						type='number'
						fullWidth
						variant='outlined'
						value={formData.subLatency}
						onChange={(e) =>
							setFormData({ ...formData, subLatency: e.target.value })
						}
						error={formErrors.has('subLatency')}
						helperText={formErrors.get('subLatency')}
					/>

					<TextField
						required
						margin='dense'
						id='mulLatency'
						label='Mul Instruction Latency'
						type='number'
						fullWidth
						variant='outlined'
						value={formData.mulLatency}
						onChange={(e) =>
							setFormData({ ...formData, mulLatency: e.target.value })
						}
						error={formErrors.has('mulLatency')}
						helperText={formErrors.get('mulLatency')}
					/>

					<TextField
						required
						margin='dense'
						id='divLatency'
						label='Div Instruction Latency'
						type='number'
						fullWidth
						variant='outlined'
						value={formData.divLatency}
						onChange={(e) =>
							setFormData({ ...formData, divLatency: e.target.value })
						}
						error={formErrors.has('divLatency')}
						helperText={formErrors.get('divLatency')}
					/>

					<TextField
						required
						margin='dense'
						id='loadLatency'
						label='Load Instruction Latency'
						type='number'
						fullWidth
						variant='outlined'
						value={formData.loadLatency}
						onChange={(e) =>
							setFormData({ ...formData, loadLatency: e.target.value })
						}
						error={formErrors.has('loadLatency')}
						helperText={formErrors.get('loadLatency')}
					/>

					<TextField
						required
						margin='dense'
						id='storeLatency'
						label='Store Instruction Latency'
						type='number'
						fullWidth
						variant='outlined'
						value={formData.storeLatency}
						onChange={(e) =>
							setFormData({ ...formData, storeLatency: e.target.value })
						}
						error={formErrors.has('storeLatency')}
						helperText={formErrors.get('storeLatency')}
					/>
				</DialogContent>
			</HorizontalContainer>
			<LoadingButton
				loading={loading}
				onClick={handleSubmit}
				sx={{
					marginTop: '20px',
					display: 'block',
					marginLeft: 'auto',
					marginRight: 'auto',
				}}
			>
				Submit
			</LoadingButton>
		</>
	);
};

export default Setup;
