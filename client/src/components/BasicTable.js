import * as React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

export default function BasicTable({ content }) {
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
				</TableBody>
			</Table>
		</TableContainer>
	);
}
