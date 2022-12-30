import './App.css';
import Setup from './pages/Setup';
import Simulation from './pages/Simulation';
import { Route, Routes } from 'react-router-dom';

function App() {
	return (
		<Routes>
			<Route path='/' element={<Setup />} />
			<Route exact path='/run' element={<Simulation />} />
		</Routes>
	);
}

export default App;
