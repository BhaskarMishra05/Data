import pandas as pd
pd.set_option('display.max_rows', None)
from src.logger import logging

def cleaning_raw_file(data_csv: str) -> pd.DataFrame:
    logging.info('Starting file cleaning')
    try:
        df = pd.read_csv(data_csv)
        logging.info('Renaming column names')
        rename_colummns = {
                'Timestamp':'survey_time', 
                'age?': 'age', 
                'industry': 'industry',
                "What is your annual salary? (You'll indicate the currency in a later question. If you are part-time or hourly":'job_title',
                ' please enter an annualized equivalent -- what you would earn if you worked the job 40 hours a week':'expected_pay(40hrs)',
                ' 52 weeks a year.)"':'annual_salary',
                "How much additional monetary compensation do you get, if any (for example, bonuses or overtime in an average year)? Please only include monetary compensation here, not the value of benefits.":'bonuses',
                'Please indicate the currency':'currency',
                'If "Other," please indicate the currency here: ':'other_currency',
                'If your income needs additional context, please provide it here:': 'income_context',
                'What country do you work in?': 'work_country',
                "If you're in the U.S., what state do you work in?": 'state(only_USA)',
                'What city do you work in?':'work_city',
                "How many years of professional work experience do you have overall?": 'overall_work_experiance',
                "How many years of professional work experience do you have in your field?":'domain_work_experiance',
                "What is your highest level of education completed?":'education_level',
                "What is your gender?":'gender', 
                "What is your race? (Choose all that apply.)":'ethinicity'
                }
    except Exception as e:
        print('Cannot Change column names',e)
    try:
        logging.info("Changing dataframe's original column names")
        df = df.rename(columns = rename_colummns)
        logging.info('Converting the Croocked csv file into fixed file')

        cleaned_file_path = '/home/bhaskar/Here_we_go_again/VS_code_ting/DATA/src/Data/fixed_data/fixed_salary_survey.csv'
        df.to_csv(cleaned_file_path, index= False)
        return df
    except Exception as e:
         print('Error during making fixed dataframe')
    logging.info('Successfully completed the File cleaning stage!')
