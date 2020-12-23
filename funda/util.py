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
    def convert_data_type( cls, df, mode='print') :
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
