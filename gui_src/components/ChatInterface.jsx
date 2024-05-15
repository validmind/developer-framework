import React, { useState, useEffect, useRef } from 'react';
import { ChakraProvider, Box, VStack, Input, Button, Text, Spinner, Collapse } from '@chakra-ui/react';
import styled from 'styled-components';
import customTheme from '../theme';
import axios from 'axios';

const ChatContainer = styled(Box)`
    max-width: 600px;
    margin: 0 auto;
    padding: 1rem;
    border: 1px solid #ccc;
    border-radius: 8px;
    background-color: #fff;
`;

const MessageContainer = styled(Box)`
    max-height: 400px;
    overflow-y: auto;
    padding: 0.5rem;
    margin-bottom: 1rem;
    border-bottom: 1px solid #ccc;
`;

const Message = styled(Text)`
    margin: 0.5rem 0;
`;

const RichMessage = ({ message }) => {
    const [isExpanded, setIsExpanded] = useState(false);

    return (
        <Box>
            <Message>{message.text}</Message>
            {message.toolCall && (
                <Box>
                    <Button onClick={() => setIsExpanded(!isExpanded)} size="sm" mt={2}>
                        {isExpanded ? 'Hide Details' : 'Show Details'}
                    </Button>
                    <Collapse in={isExpanded} animateOpacity>
                        <Box mt={2} p={2} borderWidth="1px" borderRadius="md">
                            {message.toolResult ? <Text>{message.toolResult}</Text> : <Spinner />}
                        </Box>
                    </Collapse>
                </Box>
            )}
        </Box>
    );
};

const ChatInterface = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const messagesEndRef = useRef(null);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    const handleSendMessage = async () => {
        if (input.trim() === '') return;

        const newMessage = { text: input, from: 'user' };
        setMessages(prevMessages => [...prevMessages, newMessage]);
        setInput('');

        setLoading(true);

        try {
            const response = await axios.post('/api/chat', { message: input });
            const streamedMessages = response.data;

            streamedMessages.forEach(msg => {
                if (msg.toolCall) {
                    setTimeout(() => {
                        setMessages(prevMessages =>
                            prevMessages.map(m => (m === msg ? { ...m, toolResult: 'Tool call result here' } : m))
                        );
                    }, 2000);
                }
            });

            setMessages(prevMessages => [...prevMessages, ...streamedMessages]);
        } catch (error) {
            console.error('Error sending message:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleInputChange = e => {
        setInput(e.target.value);
    };

    return (
        <ChakraProvider theme={customTheme}>
            <ChatContainer>
                <MessageContainer>
                    {messages.map((msg, index) =>
                        msg.toolCall ? (
                            <RichMessage key={index} message={msg} />
                        ) : (
                            <Message key={index} color={msg.from === 'user' ? 'blue.500' : 'gray.700'}>
                                {msg.text}
                            </Message>
                        )
                    )}
                    <div ref={messagesEndRef} />
                </MessageContainer>
                <VStack spacing={2}>
                    <Input value={input} onChange={handleInputChange} placeholder="Type your message here..." />
                    <Button onClick={handleSendMessage} isLoading={loading} colorScheme="teal">
                        Send
                    </Button>
                </VStack>
            </ChatContainer>
        </ChakraProvider>
    );
};

export default ChatInterface;
