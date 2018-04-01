import React from 'react';
import '../styles/TextSegment.css';

const TextSegment = (props) => {
	return (
		<span 
			className="text-segment"
			onClick={props.onClick}>
			{props.text}
		</span>
	);
}

export default TextSegment;