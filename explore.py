import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def main():
    data_filename = 'Seattle_Pet_Licenses.csv'
    df = pd.read_csv(data_filename)
    df['DATETIME'] = pd.to_datetime(df['License Issue Date'])
    df['YEAR'] = df['DATETIME'].dt.year
    df['MONTH'] = df['DATETIME'].dt.month
    df['DAY'] = df['DATETIME'].dt.day

    table = df.pivot_table(index='YEAR', values='License Number', columns='Species', aggfunc=np.count_nonzero)

    table = df.pivot_table(index=['YEAR', 'MONTH'], values='License Number', columns='Species',
                           aggfunc=np.count_nonzero)
    table['Cat'] = table['Cat'].cumsum()
    table['Dog'] = table['Dog'].cumsum()

    table.to_csv('cumulative_pets.csv')

    x = table.index.to_flat_index().array
    x = [f'{x[i][0]}-{x[i][1]}' for i in range(len(x))]
    y = table['Dog'].tolist()
    y_cat = table['Cat'].tolist()


    fig, ax = plt.subplots()
    plt.xticks(rotation=90)

    ax.plot(x, y)
    ax.plot(x, y_cat)
    ax.set(xlabel=None, xticklabels=[])
    ax.tick_params(bottom=False)

    plt.savefig('cat_dog_comparison.png')

    df[df['Species'] == 'Dog']['Primary Breed'].value_counts().head(10).to_csv('top_dogs.csv')
    df[df['Species'] == 'Cat']['Primary Breed'].value_counts().head(10).to_csv('top_cats.csv')





if __name__ == '__main__':
    main()
