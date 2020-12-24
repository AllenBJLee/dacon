import datetime

import pandas as pd
import numpy as np

class Utils :    
    INT_MIN_MAX = [
            {
                'MIN' : -128,
                'MAX' : 127,
                'CONVERT' : 'int8'
            },
            {
                'MIN' : -32768,
                'MAX' : 32767,
                'CONVERT' : 'int16'
            },
            {
                'MIN' : -2147483648,
                'MAX' : 2147483647,
                'CONVERT' : 'int32'
            }
        ]

    @classmethod
    def convert_data_type(cls, df, mode='print') :
        """
            automate convert data type

            @param df   DataFrame
            @param mode
                - print : just print (not convert)
                - convert : auto convert
            @remark
                int 형 컬럼을 찾아 자동으로 데이터 타입을 수정한다.
        """
        convert_column = {}
        for key in df.columns :
            if True == np.issubdtype( df[key].dtypes, np.integer ) : # 컬럼 데이터 타입이 int 면
                if 'convert' == mode :
                    for int_compare_item in cls.INT_MIN_MAX :
                        if int_compare_item['MIN'] <= df[key].min() and int_compare_item['MAX'] >= df[key].max() :
                            convert_column[key] = int_compare_item['CONVERT']
                            break;

                else :
                    #print mode 이거나 다른 값을 입력했을 땐 그냥 출력만 한다.
                    print( 'key: {}\n\tmin: {}\n\tmax: {}'.format( key, df[key].min(), df[key].max() ))
        
        if 'convert' == mode and 0 < len(convert_column) :
            df = df.astype(convert_column)
        
        return df

    @classmethod
    def train_test_splitter(cls, df, date_column) :
        y_bool = df[date_column] >= '2018-12-01'
        y = df[y_bool].groupby('store_id').amount.sum()
        X = df[~y_bool]
        
        train_index = y.sample(frac=0.8, random_state=85).index

        train_X = X[X.store_id.isin(train_index)]
        test_X = X[~X.store_id.isin(train_index)]

        train_y = y[y.index.isin(train_index)]
        test_y = y[~y.index.isin(train_index)]
        
        return train_X, test_X, train_y, test_y
        # bool_y = df[ date_column] >= '2018-12-01'
        
        # y = df[bool_y].groupby('store_id').amount.sum()
        # x = df[~bool_y]

        # idx_train = y.sample(frac=0.8, random_state=85).index

        # train_x = x[x.store_id.isin(idx_train)]
        # test_x  = x[~x.store_id.isin(idx_train)]

        # train_y = y[y.index.isin(idx_train)]
        # test_y  = y[~y.index.isin(idx_train)]

        # return train_x, test_x, train_y, test_y