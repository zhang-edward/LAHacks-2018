import React from 'react';

const SegmentAnalysis = (props) => {
	if (props.segment.imagePath == undefined) {
		return (
			<div>
				Click on a segment of text to see its analysis
			</div>
		);
	}
	return (
		<div>
			<img 
				alt="screen cap"
				style={{ width: 500, height: 400 }} 
				src={process.env.PUBLIC_URL + '/frames/' + props.segment.imagePath + '.jpg'}/>
			<p>Attentiveness: {props.segment.attentiveness}</p>
		</div>
	);
}

export default SegmentAnalysis;
