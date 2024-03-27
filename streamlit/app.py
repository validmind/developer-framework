import tempfile

import streamlit as st
import pandas as pd
import xgboost as xgb

import validmind as vm
from validmind.tests import list_tests, run_test as _run_test
from validmind.utils import test_id_to_name
from validmind.vm_models.test.result_wrapper import ResultWrapper


def get_test_list():
    # Get the list of available tests from the library
    # return ["Test 1", "Test 2", "Test 3"]
    return list_tests(pretty=False)


def load_dataset(df):
    # Load the dataset from the given path
    vm_dataset = vm.init_dataset(
        df,
        input_id="test_dataset",
        target_column="Exited",
        __log=False,
    )

    return vm_dataset


def load_model(model_file, vm_dataset):
    # Load the model from the given path
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as tmpfile:
        tmpfile.write(model_file.getvalue().decode("utf-8"))
        model_path = tmpfile.name

    # Load the model from the saved file
    model = xgb.XGBClassifier()
    model.load_model(model_path)

    vm_model = vm.init_model(model, __log=False)
    vm_dataset.assign_predictions(model=vm_model)

    return vm_model


# Function to run selected test on the given model and dataset
def run_test(test_id, model, dataset):
    # Run the selected test and return the result (HTML/Jupyter widget)
    result: ResultWrapper = _run_test(test_id, inputs={
        "model": model,
        "dataset": dataset
    }, show=False)
    return result


def main():
    st.title("ValidMind Testing Playground")

    # Sidebar for uploading datasets and models
    st.sidebar.header("Upload your files")
    uploaded_dataset = st.sidebar.file_uploader("Upload a dataset", type=['csv', 'xlsx'])
    uploaded_model = st.sidebar.file_uploader("Upload a model")

    st.sidebar.header("Select a Test")
    test_options = get_test_list()  # Assume your library can provide a list of tests
    selected_test = st.sidebar.selectbox("Choose a test to run", test_options)

    # Run Test button
    running_test = False
    if st.sidebar.button("Run Test"):
        running_test = True

    # Load and display the dataset
    vm_dataset = None
    if uploaded_dataset is not None:
        dataset = pd.read_csv(uploaded_dataset)
        st.write("Dataset Preview:")
        st.write(dataset.head())
        vm_dataset = load_dataset(dataset)

    edit_data = False
    def _edit_data():
        edit_data = not edit_data
    st.button("Edit Dataset", on_click=edit_data)

    if edit_data:
        st.write("Edit Dataset")
        st.data_editor(vm_dataset.df)

    # Load the model (adjust the loading mechanism to your requirements)
    vm_model = None
    if uploaded_model is not None:
        vm_model = load_model(uploaded_model, vm_dataset)

    test_result = None

    st.header("Test Output")
    if running_test:
        if uploaded_dataset is not None and uploaded_model is not None:
            with st.spinner('Running Test...'):
                test_result = run_test(selected_test, vm_model, vm_dataset)
        else:
            st.error("Please upload both a dataset and a model to run the test.")
    if test_result:
        # st.components.v1.html(test_result, height=400, scrolling=True)
        st.subheader(f"{test_id_to_name(test_result.result_id)}")
        st.markdown(test_result.result_metadata[0].get("text", ""))

        if test_result.metric.summary:
            for table in test_result.metric.summary.results:
                # Explore advanced styling
                summary_table = pd.DataFrame(table.data) \
                .style.format(precision=4) \
                .hide(axis="index") \
                .set_table_styles(
                    [
                        {
                            "selector": "",
                            "props": [
                                ("width", "100%"),
                            ],
                        },
                        {
                            "selector": "tbody tr:nth-child(even)",
                            "props": [
                                ("background-color", "#FFFFFF"),
                            ],
                        },
                        {
                            "selector": "tbody tr:nth-child(odd)",
                            "props": [
                                ("background-color", "#F5F5F5"),
                            ],
                        },
                        {
                            "selector": "td, th",
                            "props": [
                                ("padding-left", "5px"),
                                ("padding-right", "5px"),
                            ],
                        },
                    ]
                )  # add borders
                st.write(summary_table)
                # st.components.v1.html(summary_table, height=400, scrolling=True)

        if test_result.figures:
            for fig in test_result.figures:
                # print(fig.to_html())
                # st.pyplot(fig.figure)
                # st.write(fig.to_html(), unsafe_allow_html=True)
                # st.components.v1.html(fig.to_html(), height=1000, scrolling=True)
                st.plotly_chart(fig.figure)


if __name__ == "__main__":
    main()
