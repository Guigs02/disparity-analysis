import pandas as pd
import matplotlib.pyplot as plt


if __name__== '__main__':
    df = pd.read_csv("reviewers_gender.csv")
    
    df_sorted = df.drop(df.columns[[0, 1]], axis=1)
    df_sorted.to_csv("reviewers_gender.csv")
    print(df_sorted.head(20))
    # Get the repartition of each category
    values = df['gender'].value_counts(normalize=True)*100
    genders_to_include = ['female', 'male', 'unknown']
    filtered_df = df[df['gender'].isin(genders_to_include)]

    # Create the plot
    gender_counts = filtered_df['gender'].value_counts(normalize=True)
    data = gender_counts.plot(kind='bar', color=['#1f77b4', '#ff7f0e', '#2ca02c'], rot=0, grid=True)
    data.set_ylim(0, 1)
    data.bar_label(data.containers[0])

    plt.xlabel('Sex')
    plt.ylabel('Percentage')
    plt.title('Sex Parity')
    plt.show()
    