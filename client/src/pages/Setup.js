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
import SideTabs from '../components/SideTabs';

const HorizontalContainer = styled.div`
	display: flex;
	flex-direction: row;
	height: 100vh;
	width: 100vw;
	// margin: 20px;
`;

const LeftSideContainer = styled.div`
	display: flex;
	flex-direction: column;
	width: 450px;
	height: 100vh;
	background-color: #f5f5f5;
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

	const [registers, setRegisters] = useState({
		F0: {
			Register: 'F0',
			value: 0.0,
		},
		F1: {
			Register: 'F1',
			value: 0.0,
		},
		F2: {
			Register: 'F2',
			value: 0.0,
		},
		F3: {
			Register: 'F3',
			value: 0.0,
		},
		F4: {
			Register: 'F4',
			value: 0.0,
		},
		F5: {
			Register: 'F5',
			value: 0.0,
		},
		F6: {
			Register: 'F6',
			value: 0.0,
		},
		F7: {
			Register: 'F7',
			value: 0.0,
		},
		F8: {
			Register: 'F8',
			value: 0.0,
		},
		F9: {
			Register: 'F9',
			value: 0.0,
		},
		F10: {
			Register: 'F10',
			value: 0.0,
		},
		F11: {
			Register: 'F11',
			value: 0.0,
		},
		F12: {
			Register: 'F12',
			value: 0.0,
		},
		F13: {
			Register: 'F13',
			value: 0.0,
		},
		F14: {
			Register: 'F14',
			value: 0.0,
		},
		F15: {
			Register: 'F15',
			value: 0.0,
		},
		F16: {
			Register: 'F16',
			value: 0.0,
		},
		F17: {
			Register: 'F17',
			value: 0.0,
		},
		F18: {
			Register: 'F18',
			value: 0.0,
		},
		F19: {
			Register: 'F19',
			value: 0.0,
		},
		F20: {
			Register: 'F20',
			value: 0.0,
		},
		F21: {
			Register: 'F21',
			value: 0.0,
		},
		F22: {
			Register: 'F22',
			value: 0.0,
		},
		F23: {
			Register: 'F23',
			value: 0.0,
		},
		F24: {
			Register: 'F24',
			value: 0.0,
		},
		F25: {
			Register: 'F25',
			value: 0.0,
		},
		F26: {
			Register: 'F26',
			value: 0.0,
		},
		F27: {
			Register: 'F27',
			value: 0.0,
		},
		F28: {
			Register: 'F28',
			value: 0.0,
		},
		F29: {
			Register: 'F29',
			value: 0.0,
		},
		F30: {
			Register: 'F30',
			value: 0.0,
		},
		F31: {
			Register: 'F31',
			value: 0.0,
		},
	});

	const [memory, setMemory] = useState({
		0: {
			address: 0,
			value: 0.0,
		},
		1: {
			address: 1,
			value: 0.0,
		},
		2: {
			address: 2,
			value: 0.0,
		},
		3: {
			address: 3,
			value: 0.0,
		},
		4: {
			address: 4,
			value: 0.0,
		},
		5: {
			address: 5,
			value: 0.0,
		},
		6: {
			address: 6,
			value: 0.0,
		},
		7: {
			address: 7,
			value: 0.0,
		},
		8: {
			address: 8,
			value: 0.0,
		},
		9: {
			address: 9,
			value: 0.0,
		},
		10: {
			address: 10,
			value: 0.0,
		},
		11: {
			address: 11,
			value: 0.0,
		},
		12: {
			address: 12,
			value: 0.0,
		},
		13: {
			address: 13,
			value: 0.0,
		},
		14: {
			address: 14,
			value: 0.0,
		},
		15: {
			address: 15,
			value: 0.0,
		},
		16: {
			address: 16,
			value: 0.0,
		},
		17: {
			address: 17,
			value: 0.0,
		},
		18: {
			address: 18,
			value: 0.0,
		},
		19: {
			address: 19,
			value: 0.0,
		},
		20: {
			address: 20,
			value: 0.0,
		},
		21: {
			address: 21,
			value: 0.0,
		},
		22: {
			address: 22,
			value: 0.0,
		},
		23: {
			address: 23,
			value: 0.0,
		},
		24: {
			address: 24,
			value: 0.0,
		},
		25: {
			address: 25,
			value: 0.0,
		},
		26: {
			address: 26,
			value: 0.0,
		},
		27: {
			address: 27,
			value: 0.0,
		},
		28: {
			address: 28,
			value: 0.0,
		},
		29: {
			address: 29,
			value: 0.0,
		},
		30: {
			address: 30,
			value: 0.0,
		},
		31: {
			address: 31,
			value: 0.0,
		},
		32: {
			address: 32,
			value: 0.0,
		},
		33: {
			address: 33,
			value: 0.0,
		},
		34: {
			address: 34,
			value: 0.0,
		},
		35: {
			address: 35,
			value: 0.0,
		},
		36: {
			address: 36,
			value: 0.0,
		},
		37: {
			address: 37,
			value: 0.0,
		},
		38: {
			address: 38,
			value: 0.0,
		},
		39: {
			address: 39,
			value: 0.0,
		},
		40: {
			address: 40,
			value: 0.0,
		},
		41: {
			address: 41,
			value: 0.0,
		},
		42: {
			address: 42,
			value: 0.0,
		},
		43: {
			address: 43,
			value: 0.0,
		},
		44: {
			address: 44,
			value: 0.0,
		},
		45: {
			address: 45,
			value: 0.0,
		},
		46: {
			address: 46,
			value: 0.0,
		},
		47: {
			address: 47,
			value: 0.0,
		},
		48: {
			address: 48,
			value: 0.0,
		},
		49: {
			address: 49,
			value: 0.0,
		},
		50: {
			address: 50,
			value: 0.0,
		},
		51: {
			address: 51,
			value: 0.0,
		},
		52: {
			address: 52,
			value: 0.0,
		},
		53: {
			address: 53,
			value: 0.0,
		},
		54: {
			address: 54,
			value: 0.0,
		},
		55: {
			address: 55,
			value: 0.0,
		},
		56: {
			address: 56,
			value: 0.0,
		},
		57: {
			address: 57,
			value: 0.0,
		},
		58: {
			address: 58,
			value: 0.0,
		},
		59: {
			address: 59,
			value: 0.0,
		},
		60: {
			address: 60,
			value: 0.0,
		},
		61: {
			address: 61,
			value: 0.0,
		},
		62: {
			address: 62,
			value: 0.0,
		},
		63: {
			address: 63,
			value: 0.0,
		},
		64: {
			address: 64,
			value: 0.0,
		},
		65: {
			address: 65,
			value: 0.0,
		},
		66: {
			address: 66,
			value: 0.0,
		},
		67: {
			address: 67,
			value: 0.0,
		},
		68: {
			address: 68,
			value: 0.0,
		},
		69: {
			address: 69,
			value: 0.0,
		},
		70: {
			address: 70,
			value: 0.0,
		},
		71: {
			address: 71,
			value: 0.0,
		},
		72: {
			address: 72,
			value: 0.0,
		},
		73: {
			address: 73,
			value: 0.0,
		},
		74: {
			address: 74,
			value: 0.0,
		},
		75: {
			address: 75,
			value: 0.0,
		},
		76: {
			address: 76,
			value: 0.0,
		},
		77: {
			address: 77,
			value: 0.0,
		},
		78: {
			address: 78,
			value: 0.0,
		},
		79: {
			address: 79,
			value: 0.0,
		},
		80: {
			address: 80,
			value: 0.0,
		},
		81: {
			address: 81,
			value: 0.0,
		},
		82: {
			address: 82,
			value: 0.0,
		},
		83: {
			address: 83,
			value: 0.0,
		},
		84: {
			address: 84,
			value: 0.0,
		},
		85: {
			address: 85,
			value: 0.0,
		},
		86: {
			address: 86,
			value: 0.0,
		},
		87: {
			address: 87,
			value: 0.0,
		},
		88: {
			address: 88,
			value: 0.0,
		},
		89: {
			address: 89,
			value: 0.0,
		},
		90: {
			address: 90,
			value: 0.0,
		},
		91: {
			address: 91,
			value: 0.0,
		},
		92: {
			address: 92,
			value: 0.0,
		},
		93: {
			address: 93,
			value: 0.0,
		},
		94: {
			address: 94,
			value: 0.0,
		},
		95: {
			address: 95,
			value: 0.0,
		},
		96: {
			address: 96,
			value: 0.0,
		},
		97: {
			address: 97,
			value: 0.0,
		},
		98: {
			address: 98,
			value: 0.0,
		},
		99: {
			address: 99,
			value: 0.0,
		},
	});

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
					registers: registers,
					memory: memory,
				};

				console.log(requestData);

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
				<LeftSideContainer>
					<SideTabs
						registers={registers}
						setRegisters={setRegisters}
						memory={memory}
						setMemory={setMemory}
						showEdit={true}
					/>
				</LeftSideContainer>
				<div>
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
				</div>
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
				variant='contained'
			>
				Submit
			</LoadingButton>
		</>
	);
};

export default Setup;
