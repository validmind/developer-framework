import React, { useRef, useEffect } from 'react';
import ReactDOM from 'react-dom';
import { ChakraProvider } from '@chakra-ui/react';
import customTheme from './theme';

const ShadowRootWrapper = ({ children }) => {
    const containerRef = useRef(null);
    const shadowRootRef = useRef(null);

    useEffect(() => {
        if (containerRef.current) {
            const style = document.createElement('style');

            shadowRootRef.current = containerRef.current.attachShadow({ mode: 'open' });
            shadowRootRef.current.appendChild(style);

            ReactDOM.render(<ChakraProvider theme={customTheme}>{children}</ChakraProvider>, shadowRootRef.current);
        }
        return () => {
            if (shadowRootRef.current) {
                ReactDOM.unmountComponentAtNode(shadowRootRef.current);
            }
        };
    }, [children]);

    return <div ref={containerRef}></div>;
};

export default ShadowRootWrapper;
