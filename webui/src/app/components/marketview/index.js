import {
    useRef,
    useState,
    useEffect
} from 'preact/hooks';
import * as echarts from 'echarts';
import { observer } from 'mobx-react-lite';

const MarketView = observer(({
    store
}) => {

    const refChart = useRef();
    const [historyRecords, setHistoryRecords] = useState([]);
    const [chart, setChart] = useState();

    useEffect(() => {
        setHistoryRecords(store.historyRecords);
    }, [store.historyRecords])



    useEffect(() => {
        if (refChart) {
            const myChart = echarts.init(refChart.current);
            setChart(myChart)
        }
    }, [refChart]);

    useEffect(() => {

        if (chart) {
            let option = {
                xAxis: {
                    data: []
                },
                yAxis: [
                    {
                        scale: true,
                        splitArea: {
                            show: true
                        }
                    }
                ],
                dataZoom: [
                    {
                        type: 'inside',
                        start: 98,
                        end: 100,
                        minValueSpan: 10
                    },
                    {
                        show: true,
                        type: 'slider',
                        bottom: 60,
                        start: 98,
                        end: 100,
                        minValueSpan: 10
                    }
                ],
                series: []
            };

            chart.setOption(option);
        }

    }, [chart]);

    useEffect(() => {
        if (chart) {
            let option = {
                xAxis: {
                    data: historyRecords.map((v) => {
                        return v.date
                    })
                },
                series: [{
                    type: 'k',
                    data: historyRecords.map((v) => {
                        return [v.open, v.high, v.low, v.close]
                    })
                }]
            };
            chart.setOption(option);
        }
    }, [chart, historyRecords]);

    return (<div className="w-auto h-48"
        style={
            {
                height: "300px"
            }
        }
        ref={
            refChart
        }
    />);
});

export default MarketView;