# -*- encoding: utf-8 -*-

from helper.ReadDB import ReadDB
import pandas as pd
import awswrangler as wr

# 리워드 회원 대상 분류 (return 제거 대상 회원, 제거 후 회원)
class reward:
    # df : reward adid와 비교할 테이블 insert
    def __init__(self, df):
        self.df = df

    def find_reward_customer(self):
        self.ADID = wr.s3.read_parquet(
            path='s3://path/filename.parquet'
        )
        self.ADID.rename(columns={
            'str_cd':'STR_CD',
        },
            inplace=True)
        self.df.rename(columns={
            'STR_CD':'str_cd'
        },
            inplace=True)
        merge_data = pd.merge(
            self.df,
            self.ADID,
            left_on='str_cd',
            right_on='STR_CD',
            how='left')

        # 제외 대상 회원 목록
        duplicated_customer = merge_data[merge_data['STR_CD'].notnull()]

        # 제외 대상 제거 회원 목록
        true_customer = merge_data[merge_data['STR_CD'].isnull()]

        return duplicated_customer, true_customer


# 직원 분류 (return 직원 목록, 직원 제거 후 목록)
class employee:
    def __init__(self, df):
        self.df = df

    def find_thecheck_employee(self):
        # s3 path
        employee_phone = wr.s3.read_parquet(
            path='s3://path/filename.parquet'
        )
        employee_phone['phone_num'] = employee_phone['연락처'].str.replace('-','')
        phone_merge_data = pd.merge(
            self.df, employee_phone,
            left_on='df_phone',
            right_on='phone_num',
            how='left'
        )

        # 제외 대상 회원 목록
        duplicated_employee = phone_merge_data[phone_merge_data['phone_num'].notnull()]

        # 제외 대상 제거 회원 목록
        not_employee = phone_merge_data[phone_merge_data['phone_num'].isnull()]

        return duplicated_employee, not_employee


if __name__ == "__main__":
    from helper.ReadDB import ReadDB
    from helper.delete_customer import reward
    from helper.delete_customer import employee

    pg = ReadDB(db='MS')
    query = '''
    select STR_CD, TELNO as df_phone, col_3, col_4 from table_name;
    '''
    data = pg.read_query(query)

    cls = reward(data)
    find_customer, true_customer = cls.find_reward_customer()
    print(len(find_customer))

    emp = employee(true_customer)
    non_target, target = emp.find_thecheck_employee()
    print(len(non_target))
