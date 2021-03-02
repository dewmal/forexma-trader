import { observer } from 'mobx-react-lite';
import { useContext } from 'preact/hooks';
import DashboardPageUiContext from '../stores/ui/DashboardPageUiState';
export const DashboardPage = observer(() => {
    const store = useContext(DashboardPageUiContext);
    return (
        <>
            <h1>
                Dashboard View
            </h1>

            <h2>
                {store.currentTime}
            </h2>

            {/* <ProfitView /> */}

        </>
    );
});

