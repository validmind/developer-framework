import './index.css';
import React from 'react';
import ReactDOM from 'react-dom';
import { toWebComponent } from 'react-to-webcomponent';
import ChatInterface from './components/ChatInterface';
import DataTable from './components/DataTable';
import PlotlyComponent from './components/PlotlyComponent';
import MarkdownEditor from './components/MarkdownEditor';
import GridComponent from './components/GridComponent';

const ChatWebComponent = toWebComponent(ChatInterface, React, ReactDOM);
const DataTableComponent = toWebComponent(DataTable, React, ReactDOM);
const PlotlyWebComponent = toWebComponent(PlotlyComponent, React, ReactDOM);
const MarkdownEditorComponent = toWebComponent(MarkdownEditor, React, ReactDOM);
const GridWebComponent = toWebComponent(GridComponent, React, ReactDOM);

customElements.define('chat-interface', ChatWebComponent);
customElements.define('data-table-component', DataTableComponent);
customElements.define('plotly-component', PlotlyWebComponent);
customElements.define('markdown-editor-component', MarkdownEditorComponent);
customElements.define('grid-component', GridWebComponent);
