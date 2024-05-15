import React, { useMemo, useState, useEffect } from 'react';
import { ChakraProvider, Box, Table, Thead, Tbody, Tr, Th, Td, Input } from '@chakra-ui/react';
import { useTable, useFilters, useSortBy } from 'react-table';
import customTheme from '../theme';
import styled from 'styled-components';

const DefaultColumnFilter = ({ column: { filterValue, preFilteredRows, setFilter } }) => {
    const count = preFilteredRows.length;

    return (
        <Input
            value={filterValue || ''}
            onChange={e => {
                setFilter(e.target.value || undefined);
            }}
            placeholder={`Search ${count} records...`}
        />
    );
};

const EditableCell = ({ value: initialValue, row: { index }, column: { id }, updateMyData }) => {
    const [value, setValue] = useState(initialValue);

    const onChange = e => {
        setValue(e.target.value);
    };

    const onBlur = () => {
        updateMyData(index, id, value);
    };

    useEffect(() => {
        setValue(initialValue);
    }, [initialValue]);

    return <Input value={value} onChange={onChange} onBlur={onBlur} />;
};

const DataTableWrapper = styled.div`
    .table {
        width: 100%;
    }
`;

const DataTable = ({ data: initialData, comm_id }) => {
    const [data, setData] = useState(initialData);

    const updateMyData = (rowIndex, columnId, value) => {
        setData(old =>
            old.map((row, index) => {
                if (index === rowIndex) {
                    return {
                        ...row,
                        [columnId]: value,
                    };
                }
                return row;
            })
        );

        const comm = window.Jupyter.notebook.kernel.comm_manager.get_comm(comm_id);
        if (comm) {
            comm.send({ method: 'update', content: { rowIndex, columnId, value } });
        }
    };

    const columns = useMemo(() => {
        if (data.length === 0) return [];
        return Object.keys(data[0]).map(key => ({
            Header: key,
            accessor: key,
            Filter: DefaultColumnFilter,
            Cell: EditableCell,
        }));
    }, [data]);

    const defaultColumn = useMemo(
        () => ({
            Filter: DefaultColumnFilter,
            Cell: EditableCell,
        }),
        []
    );

    const {
        getTableProps,
        getTableBodyProps,
        headerGroups,
        rows,
        prepareRow,
        setFilter,
        state: { filters },
    } = useTable(
        {
            columns,
            data,
            defaultColumn,
            updateMyData,
        },
        useFilters,
        useSortBy
    );

    return (
        <ChakraProvider theme={customTheme}>
            <DataTableWrapper>
                <Box p={4} borderWidth="1px" borderRadius="lg" overflow="hidden">
                    <Table {...getTableProps()} className="table">
                        <Thead>
                            {headerGroups.map(headerGroup => (
                                <Tr {...headerGroup.getHeaderGroupProps()}>
                                    {headerGroup.headers.map(column => (
                                        <Th {...column.getHeaderProps()}>
                                            {column.render('Header')}
                                            <div>{column.canFilter ? column.render('Filter') : null}</div>
                                        </Th>
                                    ))}
                                </Tr>
                            ))}
                        </Thead>
                        <Tbody {...getTableBodyProps()}>
                            {rows.map(row => {
                                prepareRow(row);
                                return (
                                    <Tr {...row.getRowProps()}>
                                        {row.cells.map(cell => (
                                            <Td {...cell.getCellProps()}>{cell.render('Cell')}</Td>
                                        ))}
                                    </Tr>
                                );
                            })}
                        </Tbody>
                    </Table>
                </Box>
            </DataTableWrapper>
        </ChakraProvider>
    );
};

// window.DataTable = DataTable;

export default DataTable;
