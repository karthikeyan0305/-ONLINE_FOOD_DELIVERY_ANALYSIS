from data_load import load_data
from data_cleaning import clean_data
from feature_engineering import feature_engineering
from eda import run_eda
from sql_upload import upload_to_mysql
from config import CLEAN_DATA_PATH


def main():
    print("Loading data...")
    df = load_data()

    print(" Cleaning data...")
    df = clean_data(df)

    print("Feature engineering...")
    df = feature_engineering(df)

    print(" Running EDA...")
    run_eda(df)

    print(" Saving cleaned CSV...")
    df.to_csv(CLEAN_DATA_PATH, index=False)

    print(" Uploading to MySQL...")
    # upload_to_mysql(df)   # DB ready illa na comment pannalaam

    print("✅ PIPELINE COMPLETED SUCCESSFULLY")


if __name__ == "__main__":
    main()
