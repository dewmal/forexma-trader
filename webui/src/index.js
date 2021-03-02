import { DashboardPage } from './app/pages/DashbaordPage';
import './style';
import DashboardPageUiContext, { DashbboardPageUiState } from './app/stores/ui/DashboardPageUiState';



const App = () => {
	return (
		<DashboardPageUiContext.Provider value={new DashbboardPageUiState()}>
			<DashboardPage />
		</DashboardPageUiContext.Provider>
	);
};

export default App;


