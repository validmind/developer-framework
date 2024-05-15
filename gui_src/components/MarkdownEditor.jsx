import React, { useState, useEffect } from 'react';
import SimpleMDE from 'react-simplemde-editor';
import 'easymde/dist/easymde.min.css';
import { ChakraProvider, Box } from '@chakra-ui/react';
import styled from 'styled-components';
import customTheme from '../theme';

const EditorWrapper = styled.div`
    .CodeMirror {
        height: auto;
    }
`;

const MarkdownEditor = ({ initialContent, comm_id }) => {
    const [content, setContent] = useState(initialContent || '');

    useEffect(() => {
        window.Jupyter.notebook.kernel.comm_manager.register_target(comm_id, function (comm) {
            comm.on_msg(function (msg) {
                if (msg.content.data.method === 'update') {
                    setContent(msg.content.data.content);
                }
            });
        });

        return () => {
            window.Jupyter.notebook.kernel.comm_manager.unregister_target(comm_id);
        };
    }, [comm_id]);

    const handleChange = value => {
        setContent(value);
        const comm = window.Jupyter.notebook.kernel.comm_manager.get_comm(comm_id);
        if (comm) {
            comm.send({ method: 'update', content: value });
        }
    };

    return (
        <ChakraProvider theme={customTheme}>
            <Box p={4} borderWidth="1px" borderRadius="lg" overflow="hidden">
                <EditorWrapper>
                    <SimpleMDE
                        value={content}
                        onChange={handleChange}
                        options={{
                            autofocus: true,
                            spellChecker: false,
                        }}
                    />
                </EditorWrapper>
            </Box>
        </ChakraProvider>
    );
};

export default MarkdownEditor;
