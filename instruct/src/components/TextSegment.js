import React from 'react';
import '../styles/TextSegment.css';

const TextSegment = (props) => {
	return (
		<span
			className="text-segment"
			onClick={() => props.onTextSegmentSelected(props.segment)}>
			{props.segment.segmentText}
		</span>
	);
}

export default TextSegment;