import pandas as pd
import matplotlib.pyplot as plt

def process_and_save_plot(input_csv='reviewers_gender.csv', output_plot='plot.png'):
    """
    Processes the data from a CSV, generates a gender distribution plot, and saves the plot to a file.

    Parameters:
    - input_csv (str): Path to the input CSV file. Default is 'reviewers_gender.csv'.
    - output_plot (str): Path where the plot image will be saved. Default is 'plot.png'.
    """

    # Read the CSV file
    df = pd.read_csv(input_csv)
    
    # Drop the first two columns (temporarily, without altering the original CSV)
    df_sorted = df.drop(df.columns[[0, 1]], axis=1)
    
    # Get the repartition of each category
    genders_to_include = ['female', 'male', 'unknown']
    filtered_df = df[df['gender'].isin(genders_to_include)]

    # Create the plot
    gender_counts = filtered_df['gender'].value_counts(normalize=True)
    ax = gender_counts.plot(kind='bar', color=['#1f77b4', '#ff7f0e', '#2ca02c'], rot=0, grid=True)
    ax.set_ylim(0, 1)
    ax.bar_label(ax.containers[0])

    plt.xlabel('Sex')
    plt.ylabel('Percentage')
    plt.title('Sex Parity')

    # Save the plot to a file
    plt.savefig(output_plot)
