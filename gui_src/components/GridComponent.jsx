import React, { useState } from 'react';
import { ChakraProvider, Box, Button } from '@chakra-ui/react';
import GridLayout from 'react-grid-layout';
import 'react-grid-layout/css/styles.css';
import 'react-resizable/css/styles.css';
import customTheme from '../theme';
import DataTable from './DataTable';
import PlotlyComponent from './PlotlyComponent';
import MarkdownEditor from './MarkdownEditor';

const GridComponent = ({ components, onComponentRemove }) => {
    const [layout, setLayout] = useState(
        components.map((component, index) => ({
            i: index.toString(),
            x: 0,
            y: 0,
            w: 4,
            h: 2,
        }))
    );

    const componentMapping = {
        'data-table-component': props => <DataTable {...props} />,
        'plotly-component': props => <PlotlyComponent {...props} />,
        'markdown-editor-component': props => <MarkdownEditor {...props} />,
    };

    const handleRemove = index => {
        const newLayout = layout.filter(item => item.i !== index.toString());
        setLayout(newLayout);
        onComponentRemove(index);
    };

    return (
        <ChakraProvider theme={customTheme}>
            <Box p={4} borderWidth="1px" borderRadius="lg" overflow="hidden">
                <GridLayout className="layout" cols={12} rowHeight={30} width={1200} layout={layout}>
                    {components.map((component, index) => (
                        <div key={index} data-grid={{ ...layout[index] }}>
                            {componentMapping[component.type]({ ...component.props })}
                            <Button onClick={() => handleRemove(index)} colorScheme="red" size="sm">
                                Remove
                            </Button>
                        </div>
                    ))}
                </GridLayout>
            </Box>
        </ChakraProvider>
    );
};

export default GridComponent;
