# CSV Data Visualizer with Gradio

## Overview
This is a simple web-based tool that allows users to upload CSV files, explore their contents, and visualize the data using various plot types. The app is built using **Gradio**, **Pandas**, **Matplotlib**, and **Seaborn**.

## Features
- Upload a `.csv` file and preview its first few rows.
- View dataset information, including missing values and data types.
- Select features for visualization.
- Choose from multiple plot types:
  - Line Plot
  - Histogram
  - Distribution Plot
  - Scatter Plot
  - Pie Chart
- Download or share generated plots.

## Installation
To run the project locally, follow these steps:

### Prerequisites
Make sure you have **Python 3.7+** installed.

### Clone the Repository
```bash
git clone https://github.com/mhelva/gradio_data_visualization.git
```

## Requirements
All necessary dependencies are listed in the `requirements.txt` file. To install them, simply run the following command:
```bash
pip install -r requirements.txt
```

## File Structure
```
📂 csv-visualizer
├── app.py                 # Main Gradio application
├── requirements.txt       # Python dependencies
├── README.md              # Documentation
```

