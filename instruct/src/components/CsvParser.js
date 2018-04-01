import React, { Component } from 'react';
import TextSegment from './TextSegment';
import CsvParse from '@vtex/react-csv-parse'

class CsvParser extends Component {
	constructor(props) {
		super(props);
		this.state = { data: [] };
	}

	componentWillMount() {
		fetch('/data')
			.then((response) => response.json())
			.then((responseJson) => {
				console.log(responseJson);
				this.setState({ data: responseJson });
			})
			.catch((error) => {
		  		console.error(error);
			});
	}

	renderTextSegment(segment) {
		console.log("hello");
		return (
			<div>
				hello
				<TextSegment
					text={segment.segmentText}/>
			</div>
		);
	}

	render() {
		console.log(this.state.data);
		console.log("rerender");
		return (
			<div>
				
			</div>
		);
	}
}

export default CsvParser;