from finviz.screener import Screener

from typing import List, Dict
from sklearn import logger

from stocks_finviz.get_finviz_filtered_list import find_filters_symbols

PATH = '/Users/tomerkatzav/Downloads/'
FILE_NAME = 'tomer.xlsx'


def convert_to_dict(lst):
    lst = lst.split(',')
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return res_dct


def get_filters(filters):
    # type: (List[Dict]) -> List[str]
    """
    get name filters for screener
    :param filters: list of dict
    :return: str filters values
    """

    if isinstance(filters, str):
        filters = [filters]

    if len(filters) == 0:
        logger.info('No filters')
        return

    filtered_results = find_filters_symbols(filters)

    if filtered_results:
        logger.info(f'The following filters are found: {filtered_results}')
        return filtered_results
    else:
        logger.warning('No filtered results from finviz screener')
        return


input_filters = 'Industry,Stocks only (ex-Funds),Country,USA, Market Cap,-Small (under $2bln)'

filters = convert_to_dict(input_filters)
filters_finviz = get_filters(filters)
print(filters_finviz)
['ind_stocksonly', 'geo_usa', 'fa_eps5years_pos', 'ta_volatility_wo10', 'sh_relvol_o1', 'sh_outstanding_u20',
 'sh_float_u20']

export_path = PATH
file_name = FILE_NAME
try:
    stock_list = Screener(filters=filters_finviz, table='Performance', order='price')
except Exception as e:
    print(f'No stocks after screening. {e}')
    stock_list = None
# Either use finviz built in to_csv
stock_list.to_csv("stock.csv")

# Create a SQLite database
stock_list.to_sqlite("stock.sqlite3")

"""
--input_filters="Industry,Stocks only (ex-Funds),Country,USA, Market Cap,-Small (under $2bln)"
--file_name=filtered_stocks
--export_path=/Users/tomerkatzav/Downloads/
--save_csv=False
--feature_set_name=high_vol_05
"""
