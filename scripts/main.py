import pandas as pd
import numpy as np
import load_data
from generator import GenerateDate
from sort_get_time import SortGetTime


def merge(date_list, name_list):
    # 合并时间和名称
    total = []
    for date in date_list:
        for name in name_list:
            total.append((date, name))
    return total


def generate_week_day(df, date_column, flag="y"):
    if flag == "y" or "\n":
        df["day_of_week"] = df[date_column].dt.dayofweek
    else:
        pass
    return df


def generate_open(df, target_column, flag="y"):
    if flag == "y" or "\n":
        df["open"] = np.where(df[target_column] > 0, 1, 0)
    else:
        pass
    return df


def main():

    # 1.导入文件，确定日期列，填充列，目标列
    data_name = input("请输入要转化的文件全名:(例如:test.csv)\n")
    date_column = input("请输入日期所在的列名:\n")
    target_column = input("请输入预测目标所在的列名:\n")
    type_column = input("请输入需要填充的item(目前仅支持一个):\n")
    loader = load_data.LoadData()
    origin_data = loader.load_data(data_name)

    # 2.对日期列按日期排序,然后根据时间戳范围，生成完整的时间戳
    sorter = SortGetTime(origin_data, date_column)
    sorter.sort()
    sorted_data, first_day, last_day = sorter.get_time()
    sorted_data[date_column] = pd.to_datetime(sorted_data[date_column])
    generate_date = GenerateDate(first_day, last_day)
    dates = generate_date.generate()

    # 3.将时间戳和名称合并为DataFrame_1
    name_list = list(set(sorted_data[type_column]))
    if str(name_list[0]) == "nan":
        name_list.pop(0)
    else:
        pass
    merge_list = merge(dates, name_list)
    df_merge = pd.DataFrame(merge_list, columns=[date_column, type_column])

    # 4.将DataFrame_1和原来的DataFrame外连接合并
    df_total = pd.merge(df_merge, sorted_data, how="outer", on=[date_column, type_column])

    # 5.额外选项
    df_total[date_column] = pd.to_datetime(df_total[date_column])
    week_day_flag = input("是否需要生成星期几: y(Default)/n\n")
    generate_week_day(df_total, date_column, week_day_flag)
    open_flag = input("是否需要生成open: y(Default)/n\n")
    generate_open(df_total, target_column, open_flag)
    df_total = df_total.fillna(0)
    print(df_total.head())

    # 6.导出
    export_name_first = data_name.split(".")[0] + "_out"
    export_name_end = data_name.split(".")[-1]
    export_name = export_name_first + "." + export_name_end
    df_total.to_excel(export_name, index_label="ID")


if __name__ == "__main__":
    main()
