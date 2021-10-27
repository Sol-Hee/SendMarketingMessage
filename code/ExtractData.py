# library import
import pandas as pd
from helper import ReadDB
from helper import delete_customer
from io import StringIO
import io
import boto3
import datetime
from customizing import query

today = datetime.date.today()


# Read Query
def extract():
    query = query.query

    pg = ReadDB.ReadDB()
    agree = pg.read_query(query)

    agree.rename(
        columns={
            'adid': 'ADID',
            'telno': 'df_phone'
        },
        inplace=True)

    cls = delete_customer.reward(agree)
    find_customer, true_customer = cls.find_reward_customer()

    emp = delete_customer.employee(true_customer)
    non_target, target = emp.find_thecheck_employee()

    select_columns = [
        'col_1',
        'col_2',
        'col_3',
        'col_4'
    ]
    select_columns_in_target = target[select_columns].copy()

    # save in s3
    bucket = 'your_bucket'
    with io.BytesIO() as output:
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            select_columns_in_target.to_excel(writer)
        data = output.getvalue()

    s3_resource = boto3.resource('s3')
    s3_resource.Object(bucket, f'your_key/excel-{today}.xlsx').put(Body=data)
    return None