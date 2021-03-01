import DashboardPage from './app/pages/DashbaordPage';
import './style';
import { observer } from "mobx-react-lite"


const App = observer(() => {
	return (
		<DashboardPage />
	);
});

export default App;


