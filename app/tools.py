# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/1/8 15:27
# IDE：PyCharm

import re

def get_standard_name(new_name):
    return str(new_name).strip() if (
        (new_name is not None) and len(str(new_name).strip()) > 0) else None


# 从datetime中重建构造datetime_local所需要的的格式
def reform_datetime_local_with_datetime(datetime):
    result = str(datetime.year)
    result += "-"+add_zero_for_month_day_hour_minute(datetime.month)
    result  += "-"+add_zero_for_month_day_hour_minute(datetime.day)
    result += "T" + add_zero_for_month_day_hour_minute(datetime.hour)
    result += ":" + add_zero_for_month_day_hour_minute(datetime.minute)
    return result


# 如果月日时分秒只有一位数字，则给它前面加一个0
def add_zero_for_month_day_hour_minute(time_unit):
    if len(str(time_unit)) == 1:
        time_unit = "0"+str(time_unit)
    return str(time_unit)


# 获取文件类型
def get_file_type(file_name):
    return str(file_name).rsplit('.', 1)[1]


# 字符串是否是时间戳
def is_timestamp(string):
    pattern = re.compile("^[1-2][0-9]{3}-[01][0-9]-[0-3][0-9] [0-2][0-9]:[0-5][0-9]:[0-5][0-9]$")
    if pattern.match(str(string).strip()):
        return True
    return False

def is_date(string):
    pattern = re.compile("^[1-2][0-9]{3}-[01][0-9]-[0-3][0-9]$")
    if pattern.match(str(string).strip()):
        return True
    return False