import React from 'react';
import styled from 'styled-components';
import CodeMirror from '@uiw/react-codemirror';
import { javascript } from '@codemirror/lang-javascript';

const Container = styled.div`
	display: flex;
	flex-direction: column;
	width: 500px;
`;

const FileEditor = ({ code, setCode }) => {
	const handleChange = (event) => {
		const file = event.target.files[0];

		if (file) {
			const reader = new FileReader();
			reader.onload = (event) => {
				const fileContent = event.target.result;
				setCode(fileContent);
			};
			reader.readAsText(file);
		}
	};
	const onChange = React.useCallback((value, viewUpdate) => {
		setCode(value);
	}, []);

	return (
		<Container>
			<CodeMirror
				value={code}
				height='400px'
				extensions={[javascript({ jsx: true })]}
				onChange={onChange}
				theme='dark'
			/>

			<br />
			<input type='file' onChange={handleChange} />
		</Container>
	);
};

export default FileEditor;
