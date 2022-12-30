import * as React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

// const columnNames = ['Register', 'Value'];

const content = {
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
};

const A = {
	A1: {
		busy: false,
		op: 'ADD.D',
		vj: 1.0,
		vk: 1.0,
		qj: null,
		qk: null,
		time: 0,
		state: 'writing back',
		output: 2.0,
		tag: 'A1',
	},
	A2: {
		busy: false,
		op: null,
		vj: null,
		vk: null,
		qj: null,
		qk: null,
		time: -1,
		state: 'issued',
		output: null,
		tag: 'A2',
	},
	A3: {
		busy: false,
		op: null,
		vj: null,
		vk: null,
		qj: null,
		qk: null,
		time: -1,
		state: 'issued',
		output: null,
		tag: 'A3',
	},
};

export default function BasicTable({ content }) {
	// Object.values(content).map((value, index) => {
	// 	Object.keys(value).map((key, index2) => {
	// 		console.log(key);
	// 	});
	// });

	const getColumnNames = (content) => {
		let columnNames = [];
		const firstRow = Object.values(content)[0];
		Object.keys(firstRow).map((key, index) => {
			columnNames.push(key);
		});
		return columnNames;
	};

	const columnNames = getColumnNames(content);

	return (
		<TableContainer sx={{ maxHeight: '80vh' }} component={Paper}>
			<Table aria-label='simple table'>
				<TableHead>
					<TableRow>
						{columnNames.map((name, index) => (
							<TableCell key={index}>{name}</TableCell>
						))}

						{/* {columnNames.map((name, index) => (
							<TableCell key={index}>{name}</TableCell>
						))} */}
					</TableRow>
				</TableHead>
				<TableBody>
					{Object.values(content).map((value, index) => (
						<TableRow key={index}>
							{Object.values(value).map((value2, index2) => (
								<TableCell key={index2}>{JSON.stringify(value2)}</TableCell>
							))}
						</TableRow>
					))}

					{/* {Object.entries(content).map(([key, value], index) => (
						<TableRow key={index}>
							<TableCell>{key}</TableCell>
							<TableCell>{value}</TableCell>
						</TableRow>
					))} */}
				</TableBody>
			</Table>
		</TableContainer>
	);
}

BasicTable.defaultProps = {
	// columnNames,
	content: A,
};
