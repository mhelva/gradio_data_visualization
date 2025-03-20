import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import gradio as gr
import numpy as np


def info_table(dataframe):
    n_miss = dataframe.isnull().sum().sort_values(ascending=False)
    ratio = (dataframe.isnull().sum() / dataframe.shape[0] * 100).sort_values(ascending=False)
    unique_count = dataframe.nunique()
    dtype = dataframe.dtypes
    info_df = pd.concat([n_miss, np.round(ratio, 2), unique_count, dtype],
                        axis=1, keys=['missing_values', 'missing_ratio', 'unique_values', 'dtype'])
    return info_df.reset_index()

def get_columns(file):
    if file is None:
        return gr.Dropdown(choices=[]), gr.Dropdown(choices=[])

    try:
        df = pd.read_csv(file.name)
        columns = df.columns.tolist()
        df.head()
        return gr.Dropdown(choices=columns, value=columns[0] if columns else None), \
            gr.Dropdown(choices=columns,
                               value=columns[1] if len(columns) > 1 else columns[0] if columns else None), \
            info_table(df), df.head()
    except Exception as e:
        return gr.Dropdown(choices=[], value=None), gr.Dropdown(choices=[], value=None)


def plot_csv(file, x_column, y_column, plot_type):
    if file is None:
        return "Please upload a CSV file."

    try:
        df = pd.read_csv(file.name)

        if x_column not in df.columns or y_column not in df.columns:
            return f"Columns not found: {x_column}, {y_column}"

        plt.figure(figsize=(10, 6))

        if plot_type == "Line Plot":
            plt.plot(df[x_column], df[y_column])
            plt.xlabel(x_column)
            plt.ylabel(y_column)
            plt.title(f"Line Plot of {y_column} vs {x_column}")


        elif plot_type == "Histogram":
            plt.hist(df[y_column], bins=30)  # Or another number of bins.
            plt.xlabel(y_column)
            plt.ylabel("Frequency")
            plt.title(f"Histogram of {y_column}")

        elif plot_type == "Distribution":
            sns.distplot(df[y_column], bins=30, kde=True)
            plt.xlabel(y_column)
            plt.ylabel("Density")
            plt.title(f"Distribution of {y_column}")

        elif plot_type == "Scatter Plot":
            plt.scatter(df[x_column], df[y_column])
            plt.xlabel(x_column)
            plt.ylabel(y_column)
            plt.title(f"Scatter Plot of {y_column} vs {x_column}")


        elif plot_type == "Pie Chart":
            counts = df[y_column].value_counts()
            plt.pie(counts, labels=counts.index, autopct='%1.1f%%')
            plt.title(f"Pie Chart of {y_column}")

        plot_path = "plot.png"
        plt.savefig(plot_path)
        plt.close()
        return plot_path

    except Exception as e:
        return f"Error while plotting: {e}"

# Gradio Interface
with gr.Blocks() as interface:
    gr.Markdown("# Upload Your Data and Visualize")

    file_input = gr.File(label="Upload a .csv File")
    gr.Markdown("## Dataset Info and Preview")
    dataset_head = gr.DataFrame()
    column_info = gr.DataFrame()
    column_selector_x = gr.Dropdown([], label="Select X-axis Feature")
    column_selector_y = gr.Dropdown([], label="Select Y-axis Feature")
    note = gr.Markdown("For Histogram, Distribution and Pie Chart choose only the Y-axis feature.")
    plot_type_selector = gr.Radio(["Line Plot", "Histogram", "Distribution", "Scatter Plot", "Pie Chart"], label="Select Plot Type",
                                  value="Line Plot")
    plot_button = gr.Button("Plot")
    output_plot = gr.Image(type="filepath")

    file_input.change(fn=get_columns, inputs=file_input, outputs=[column_selector_x, column_selector_y,
                                                                  column_info, dataset_head])
    plot_button.click(fn=plot_csv, inputs=[file_input, column_selector_x, column_selector_y, plot_type_selector],
                      outputs=output_plot)

interface.launch(share=True)