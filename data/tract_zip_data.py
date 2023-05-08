import pandas as pd


def main():
    # read data
    tract_zip_data_filename = 'TRACT_ZIP_122021.xlsx'
    df = pd.read_excel(tract_zip_data_filename)
    df = df[df['usps_zip_pref_city'] == 'SEATTLE']

    # get unique tracts
    unique_tracts = df['tract'].drop_duplicates().tolist()

    # select highest total ratio for FIPS -> zip conversion
    df_unique_tracts = []
    for tract in unique_tracts:
        df_tract = df[df['tract'] == tract]

        if df_tract.shape[0] > 1:
            df_tract = df_tract.sort_values(by='tot_ratio', ascending=False)
            df_unique_tracts.append(df_tract.iloc[[0]])
        elif df_tract.shape[0] == 1:
            df_unique_tracts.append(df_tract)


    # output data
    df_out = pd.concat(df_unique_tracts)
    df_out.to_csv('tract_zip_data.csv')


if __name__ == '__main__':
    main()
