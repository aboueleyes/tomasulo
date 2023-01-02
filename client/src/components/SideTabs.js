import { useState } from 'react';
import BasicTable from './BasicTable';
import BasicTabs from './Tabs';
import * as Yup from 'yup';
import { Button, TextField } from '@mui/material';
import validateFormData from '../utils/validateFormData';

const SideTabs = ({ registers, setRegisters, memory, setMemory, showEdit }) => {
	const [registerNumber, setRegisterNumber] = useState(0);
	const [registerValue, setRegisterValue] = useState(0);

	const [registerErrors, setRegisterErrors] = useState(new Map());

	const registerValidationRules = {
		registerNumber: Yup.number().required().min(0).max(31),
		registerValue: Yup.number().required(),
	};

	const [memoryAddress, setMemoryAddress] = useState(0);
	const [memoryValue, setMemoryValue] = useState(0.0);

	const [memoryErrors, setMemoryErrors] = useState(new Map());

	const memoryValidationRules = {
		memoryAddress: Yup.number().required().min(0).max(99),
		memoryValue: Yup.number().required(),
	};

	return (
		<BasicTabs
			tabNames={['Register File', 'Memory']}
			components={[
				<>
					<BasicTable content={registers} />
					{showEdit && (
						<div
							style={{
								backgroundColor: '#fff',
								padding: '10px',
								borderRadius: '5px',
								marginTop: '10px',
							}}
						>
							<div
								style={{
									display: 'flex',
									flexDirection: 'row',
								}}
							>
								<TextField
									required
									autoFocus
									margin='dense'
									id='registerNumber'
									label='Register number'
									type='number'
									fullWidth
									variant='outlined'
									value={registerNumber}
									onChange={(e) => setRegisterNumber(e.target.value)}
									error={registerErrors.has('registerNumber')}
									helperText={registerErrors.get('registerNumber')}
								/>
								<TextField
									required
									autoFocus
									margin='dense'
									id='registerValue'
									label='Register Value'
									type='number'
									fullWidth
									variant='outlined'
									value={registerValue}
									onChange={(e) => setRegisterValue(e.target.value)}
									error={registerErrors.has('registerValue')}
									helperText={registerErrors.get('registerValue')}
								/>
							</div>
							<Button
								onClick={() => {
									setRegisterErrors(new Map());
									validateFormData(
										{ registerNumber, registerValue },
										registerValidationRules
									)
										.then(() => {
											setRegisters({
												...registers,
												[`F${registerNumber}`]: {
													Register: `F${registerNumber}`,
													value: Number(registerValue),
												},
											});
										})
										.catch((errors) => {
											setRegisterErrors(errors);
										});
								}}
								variant='contained'
								style={{
									width: '100%',
								}}
							>
								Change
							</Button>
						</div>
					)}
				</>,
				<>
					<BasicTable content={memory} />
					{showEdit && (
						<div
							style={{
								backgroundColor: '#fff',
								padding: '10px',
								borderRadius: '5px',
								marginTop: '10px',
							}}
						>
							<div
								style={{
									display: 'flex',
									flexDirection: 'row',
								}}
							>
								<TextField
									required
									autoFocus
									margin='dense'
									id='memoryAddress'
									label='Memory address'
									type='number'
									fullWidth
									variant='outlined'
									value={memoryAddress}
									onChange={(e) => setMemoryAddress(e.target.value)}
									error={memoryErrors.has('memoryAddress')}
									helperText={memoryErrors.get('memoryAddress')}
								/>
								<TextField
									required
									autoFocus
									margin='dense'
									id='memoryValue'
									label='Memory Value'
									type='number'
									fullWidth
									variant='outlined'
									value={memoryValue}
									onChange={(e) => setMemoryValue(e.target.value)}
									error={memoryErrors.has('memoryValue')}
									helperText={memoryErrors.get('memoryValue')}
								/>
							</div>
							<Button
								onClick={() => {
									setMemoryErrors(new Map());
									validateFormData(
										{ memoryAddress, memoryValue },
										memoryValidationRules
									)
										.then(() => {
											setMemory({
												...memory,
												[`${memoryAddress}`]: {
													address: Number(memoryAddress),
													value: Number(memoryValue),
												},
											});
										})
										.catch((errors) => {
											setMemoryErrors(errors);
										});
								}}
								variant='contained'
								style={{
									width: '100%',
								}}
							>
								Change
							</Button>
						</div>
					)}
				</>,
			]}
		/>
	);
};

export default SideTabs;
