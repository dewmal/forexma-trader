import { observer } from 'mobx-react-lite';
import { useContext, useEffect } from 'preact/hooks';
import { globalContext } from '../stores/rootStore';


const MarketStatusAskPrice = observer(({ store }) => {
    return (<>Ask {(store && store.marketStatus) && <span>{store.marketStatus.ask}</span>}</>);
})


const MarketStatusBidPrice = observer(({ store }) => {
    return (<>Bid {(store && store.marketStatus) && <span>{store.marketStatus.bid}</span>}</>);
})

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
            </h2>

            {/* <ProfitView /> */}

        </>
    );
});

