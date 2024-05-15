import React from 'react';
import ReactDOM from 'react-dom';
import DataTable from './components/DataTable';

window.VMComponents = {
    DataTable,
};

// Exporting React and ReactDOM for use in the global scope
window.React = React;
window.ReactDOM = ReactDOM;
