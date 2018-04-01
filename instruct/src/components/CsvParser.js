import React, { Component } from 'react';
import TextSegment from './TextSegment';
import SegmentAnalysis from './SegmentAnalysis';
import '../styles/CsvParser.css';

class CsvParser extends Component {
	constructor(props) {
		super(props);
		this.state = { 
			data: [],
			selectedSegment: {}
		};
	}

	componentWillMount() {
		fetch('/data')
			.then((response) => response.json())
			.then((responseJson) => {
				console.log("Response: ");
				console.log(responseJson.data)
				this.setState({ data: responseJson.data });
			})
			.catch((error) => {
		  		console.error(error);
			});
	}

	renderSegment = (segment) => {
		return (
			<TextSegment
				onTextSegmentSelected={segment => this.setState({ selectedSegment: segment }) }
				key={segment.pathToImage}
				segment={segment}/>
		);
	}

	render() {
		console.log(this.state.selectedSegment);
		return (
			<div className="container">
				<div className="container-child">
					<p><u>Transcript</u></p>
					{this.state.data.map(this.renderSegment)}
				</div>
				<div className="container-child">
					<p><u>Analysis</u></p>
					<SegmentAnalysis segment={this.state.selectedSegment}/>
				</div>
			</div>

		);
	}
}

export default CsvParser;