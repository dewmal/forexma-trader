import './style';
import { useRef, useState, useEffect } from 'preact/hooks';
import * as echarts from 'echarts';


export default function App() {
	const refChart = useRef();
	const [chart, setChart] = useState();

	useEffect(() => {
		if (refChart) {
			const myChart = echarts.init(refChart.current);			
			console.log(setChart);
			setChart(myChart)
		}
	}, [refChart]);

	useEffect(() => {
		if (chart) {
			let option = {
				xAxis: {
					type: 'category',
					data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
				},
				yAxis: {
					type: 'value'
				},
				series: [{
					data: [150, 230, 224, 218, 135, 147, 260],
					type: 'line'
				}]
			};
			chart.setOption(option);
		}
	}, [chart]);

	return (
		<div className="bg-red-400">
			<h1>Hello, World!</h1>

			<div className="w-auto h-48" style={{ height: "300px" }} ref={refChart} />
		</div>
	);
}

