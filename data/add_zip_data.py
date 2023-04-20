import pandas as pd
import os
import shutil


def add_zip_data(df_data: pd.DataFrame, df_zip_tracts: pd.DataFrame) -> pd.DataFrame:
    df_data = df_data.merge(df_zip_tracts, left_on='Geographic Identifier - FIPS Code', right_on='tract')
    return df_data

def drop_excluded(items: list, exclusions: list) -> list:
    out = []
    for item in items:
        if not any(substr in item for substr in exclusions):
            out.append(item)
    return out


def main():
    # import census tract information
    zip_tracts_filename = 'zip_tracts_seattle.csv'
    df_tracts = pd.read_csv(zip_tracts_filename)
    df_tracts = df_tracts.filter(items=['zip', 'tract'], axis='columns')

    # get csv files in directory
    current_directory = os.getcwd()
    output_directory_name = 'zip_code_added'
    excluded_csv_files = ['TRACT', 'zip_tracts', 'temp', 'Pet_Licenses']
    csv_files = [i for i in os.listdir(os.getcwd()) if 'csv' in i]
    csv_files = drop_excluded(csv_files, excluded_csv_files)

    # make output directory
    try:
        shutil.rmtree(output_directory_name)
        os.mkdir(output_directory_name)
    except FileNotFoundError:
        os.mkdir(output_directory_name)

    # add zip code data and output result
    for file in csv_files:
        print(f'Processing: {file}')
        output_filename = file.replace('.csv', '_zip_added.csv')
        df = pd.read_csv(file)
        df = add_zip_data(df, df_tracts)
        os.chdir(current_directory+'\\'+output_directory_name)
        df.to_csv(output_filename)
        os.chdir(current_directory)


if __name__ == '__main__':
    main()
