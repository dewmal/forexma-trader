import "preact/debug"; // <-- Add this line at the top of your main entry file
import { DashboardPage } from './app/pages/DashbaordPage';
import './style';
import { GlobalProvider } from "./app/stores/rootStore";



const App = () => {
	return (

		<GlobalProvider>
			<DashboardPage />
		</GlobalProvider>

		// <DashboardPageUiContext.Provider value={defaultDashbboardPageUiState}>
		// 	<DashboardPage />
		// </DashboardPageUiContext.Provider>
	);
};

export default App;


