import pandas as pd
import numpy as np
import load_data
from generator import GenerateDate
from get_time import GetTime


def merge(date_list, name_list):
    # 合并时间和名称
    total = []
    for date in date_list:
        for name in name_list:
            total.append((date, name))
    return total


def generate_week_day(df, date_column, flag="y"):
    if flag == "y" or flag == "":
        print("添加day_of_week列...")
        df["day_of_week"] = df[date_column].dt.dayofweek
    else:
        pass
    return df


def generate_open(df, target_column, flag="y"):
    if flag == "y" or flag == "":
        print("添加open列...")
        df["open"] = np.where(df[target_column] > 0, 1, 0)
    else:
        pass
    return df


def feature_process(factory_name, target_column, gap=7):
    print("正在生成统计学特征：Lag, Mean, Std, Median")
    for i in range(len(factory_name)):
        num_list = factory_name[i][target_column]
        lag_list = [0] * len(factory_name[i])
        mean_list = [0] * len(factory_name[i])
        # mean_list = lag_list.copy()
        std_list = mean_list.copy()
        median_list = mean_list.copy()
        j = 0
        while j < (len(num_list) - gap):
            lag_list[j + gap] = float(num_list[j:j + 1])
            mean_list[j + gap] = np.mean(num_list[j:j + gap])
            std_list[j + gap] = np.std(num_list[j:j + gap])
            median_list[j + gap] = np.median(num_list[j:j + gap])
            j += 1
        lag = pd.DataFrame(lag_list, columns=["Lag"])
        mean = pd.DataFrame(mean_list, columns=["Mean"])
        std = pd.DataFrame(std_list, columns=["Stdev"])
        median = pd.DataFrame(median_list, columns=["Median"])
        old = factory_name[i].reset_index().drop(columns="index")
        factory_name[i] = pd.concat([old, lag, mean, std, median], axis=1)


def main():
    # 1.导入文件，确定日期列，填充列，目标列
    data_name = input("请输入要转化的文件全名:(例如:all_in_one.csv)\n")
    date_column = input("请输入日期所在的列名:\n")
    target_column = input("请输入预测目标所在的列名:\n")
    type_column = input("请输入需要填充的item(目前仅支持一个):\n")
    loader = load_data.LoadData()
    origin_data = loader.load_data(data_name)

    # 2.根据时间戳范围，生成完整的时间戳
    timer = GetTime(origin_data, date_column)
    data, first_day, last_day = timer.get_time()
    data[date_column] = pd.to_datetime(data[date_column])
    generate_date = GenerateDate(first_day, last_day)
    dates = generate_date.generate()

    # 3.将时间戳和名称合并为DataFrame_1
    name_list = list(set(data[type_column]))
    if str(name_list[0]) == "nan":
        name_list.pop(0)
    else:
        pass
    merge_list = merge(dates, name_list)
    df_merge = pd.DataFrame(merge_list, columns=[date_column, type_column])

    # 4.将DataFrame_1和原来的DataFrame外连接合并
    df_total = pd.merge(df_merge, data, how="outer", on=[date_column, type_column])

    # 5.额外选项
    df_total[date_column] = pd.to_datetime(df_total[date_column])
    week_day_flag = input("是否需要生成星期几: y(Default)/n\n")
    generate_week_day(df_total, date_column, week_day_flag)
    open_flag = input("是否需要生成open: y(Default)/n\n")
    generate_open(df_total, target_column, open_flag)
    print("Filling N/A...")
    df_total = df_total.fillna(0)
    print(df_total.head())

    # 6.特征工程
    feature_flag = input("是否添加统计学特征: y(Default)/n\n")
    if feature_flag == "y" or feature_flag == "":
        period = input("请输入统计学特征间隔时间(Default:7):\n")
        factory_name = []
        for i in range(len(name_list)):
            factory_name.append(df_total[i::len(name_list)])
        if period == "":
            feature_process(factory_name, target_column)
        else:
            feature_process(factory_name, target_column, int(period))
        df_total = pd.concat(factory_name, axis=0)
        df_total = df_total.sort_values(by=[date_column, type_column])
        df_total = df_total.reset_index().drop(columns="index")
    else:
        pass

    # 6.导出
    export_name_first = data_name.split(".")[0] + "_out"
    export_name_end = data_name.split(".")[-1]
    export_name = export_name_first + "." + export_name_end
    if export_name_end == "xlsx":
        df_total.to_excel(export_name, index_label="ID")
    elif export_name_end == "csv":
        df_total.to_csv(export_name, index_label="ID")
    else:
        pass


if __name__ == "__main__":
    main()
