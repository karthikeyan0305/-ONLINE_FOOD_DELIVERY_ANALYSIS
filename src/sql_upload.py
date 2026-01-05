from sqlalchemy import create_engine
from config import MYSQL

def upload_to_mysql(df):

    engine = create_engine(MYSQL)
    df.to_sql(
        "food_orders",
        engine,
        if_exists="replace",
        index=False
    )

    print("Data uploaded to mysql")