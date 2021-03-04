import { observer } from 'mobx-react-lite';
import { useContext, useEffect } from 'preact/hooks';
import MarketView from '../components/marketview';
import { globalContext } from '../stores/rootStore';

const MarketStatusTime = observer(({ store }) => {
    return (<>Date {(store && store.marketStatus) && <span>{store.marketStatus.date}</span>}</>);
});

const MarketStatusAskPrice = observer(({ store }) => {
    return (<>Ask {(store && store.marketStatus) && <span>{store.marketStatus.ask}</span>}</>);
});

const MarketStatusBidPrice = observer(({ store }) => {
    return (<>Bid {(store && store.marketStatus) && <span>{store.marketStatus.bid}</span>}</>);
});

export const DashboardPage = observer(() => {
    const store = useContext(globalContext);
    const { uiStore } = store;

    useEffect(() => {
        uiStore.startSocket();
        uiStore.readSocket();
    }, [uiStore])

    return (
        <>
            <h1>
                Dashboard View
            </h1>

            <h2>
                <MarketStatusAskPrice store={uiStore} />
                <MarketStatusBidPrice store={uiStore} />
                <MarketStatusTime store={uiStore} />
            </h2>

            <MarketView store={uiStore} />

        </>
    );
});

