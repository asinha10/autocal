import pandas as pd
from pandas.tseries.holiday import *
from pandas.tseries.offsets import CustomBusinessDay
from pandas.tseries.offsets import MonthEnd
import datetime as dt
import itertools


# This function will return a list of dictionary with Calendar dates
def generate_cal_f(holidays):
    # Create a custom Calender with custom Holiday List
    sei_wd_cal = CustomBusinessDay(holidays=holidays)
    v_start_date = holidays[0]

    # Create a dictionary to hold the list of all dates by each month
    wd_dict = {}
    cd_dict = {}

    # function to return a list of business days based on custom calendar
    def calc_business_days(start_dt, end_dt):
        dys_list = []
        for dys in pd.date_range(start=start_dt, end=end_dt, freq=sei_wd_cal):
            dts = datetime.strftime(dys, '%Y-%m-%d')
            dys_list.append(dts)

        return dys_list

    # function to return a list of calendar days
    def calc_cal_days(start_dt, end_dt):
        dys_list = []
        for dys in pd.date_range(start=start_dt, end=end_dt):
            dts = datetime.strftime(dys, '%Y-%m-%d')
            dys_list.append(dts)

        return dys_list

    # Create a dictionary with list of monthly business dates
    for month_num in pd.date_range(start=v_start_date, periods=12, freq='MS'):
        # Loop for the entire year
        month_start_date = month_num.strftime("%Y-%m-%d")
        end_date_list = pd.date_range(start=month_num, periods=1, freq='M').strftime("%Y-%m-%d")
        month_end_date = end_date_list.values[0]
        for monthly_date in pd.date_range(month_start_date, month_end_date, freq='MS'):
            # Loop for each month in the year
            start_date = monthly_date.strftime("%Y-%m-%d")
            end_date = (monthly_date + MonthEnd(1))
            dy_list = calc_business_days(start_date, end_date)

        mnth_year = dt.datetime.strptime(month_start_date, "%Y-%m-%d")
        month_key = mnth_year.strftime('%b')
        yr_key = mnth_year.strftime('%y')
        dict_key = f'{month_key}-{yr_key}'
        # add the monthly list to the dictionary
        wd_dict[dict_key] = dy_list

    # print(wd_dict)

    # Create a dictionary with list of monthly Calendar dates
    for month_num in pd.date_range(start=v_start_date, periods=12, freq='MS'):
        # Loop for the entire year
        month_start_date = month_num.strftime("%Y-%m-%d")
        end_date_list = pd.date_range(start=month_num, periods=1, freq='M').strftime("%Y-%m-%d")
        month_end_date = end_date_list.values[0]
        for monthly_date in pd.date_range(month_start_date, month_end_date, freq='MS'):
            # Loop for each month in the year
            start_date = monthly_date.strftime("%Y-%m-%d")
            end_date = (monthly_date + MonthEnd(1))
            dy_list = calc_cal_days(start_date, end_date)

        mnth_year = dt.datetime.strptime(month_start_date, "%Y-%m-%d")
        month_key = mnth_year.strftime('%b')
        yr_key = mnth_year.strftime('%y')
        dict_key = f'{month_key}-{yr_key}'
        # add the monthly list to the dictionary
        cd_dict[dict_key] = dy_list

    # print(cd_dict)
    #############################
    # not being used
    # Create a dictionary with list of Weekly calendar dates
    def get_week_dates(start_dt, offset):
        wk_dict = {}
        for dt_range in pd.date_range(start=start_dt, periods=12, freq='MS'):
            end_dt_list = pd.date_range(start=dt_range, periods=1, freq='M').strftime("%Y-%m-%d")
            month_start_dt = dt_range.strftime("%Y-%m-%d")
            month_end_dt = end_dt_list.values[0]
            wk_list = []
            for wk_dt in pd.date_range(month_start_dt, month_end_dt, freq=offset):
                get_wk_dt = wk_dt.strftime("%Y-%m-%d")
                wk_list.append(get_wk_dt)

            period_name = dt.datetime.strptime(month_start_dt, "%Y-%m-%d")
            period_name_month = period_name.strftime('%b')
            period_name_yr = period_name.strftime('%y')
            period_key = f'{period_name_month}-{period_name_yr}'

            wk_dict[period_key] = wk_list

        return wk_dict

    # print(get_week_dates('v_start_date', 'W-SUN'))

    ####################################################################################
    # function to derive business days based on specific calendar logic
    def calc_wd_dates(frequency, skip_days):
        cal_dict = {}
        if frequency[0] != '0':
            for key in wd_dict:
                cal_list = []
                for wd in frequency:
                    cal_list.append(wd_dict[key][int(wd)-1])

                cal_dict[key] = cal_list

        elif frequency[0] == '0':
            for key in wd_dict:
                i = 1
                for day in skip_days:
                    cal_list = wd_dict[key]
                    cal_list.pop(int(day)-i)
                    i = i + 1

                cal_dict[key] = cal_list

        return cal_dict

    #################################################################
    # function to derive calendar days based on specific calendar logic
    def calc_cd_dates(frequency, skip_sat, skip_sun):
        cal_dict = {}
        if skip_sun != 0:
            weekday = 6
        if skip_sat != 0:
            weekday = 5

        for key in cd_dict:
            cal_list = []
            for cd in frequency:
                if skip_sun != 0 or skip_sat != 0:
                    day_of_week = dt.datetime.strptime(cd_dict[key][int(cd) - 1], '%Y-%m-%d')
                    if (dt.date.weekday(day_of_week)) == weekday:
                        skip_back_sun = skip_sun - 1
                        cal_list.append(cd_dict[key][int(cd) + skip_back_sun])
                    else:
                        cal_list.append(cd_dict[key][int(cd) - 1])
                else:
                    cal_list.append(cd_dict[key][int(cd) - 1])

            cal_dict[key] = cal_list

        return cal_dict

    #################################################################
    # function to derive Business and Calendar days based on specific calendar logic
    def calc_both_days(wd_frequency, cd_frequency, skip_sat, skip_sun):
        w_cal_dict = {}
        c_cal_dict = {}
        for key in wd_dict:
            cal_list = []
            for wd in wd_frequency:
                cal_list.append(wd_dict[key][int(wd)-1])

            w_cal_dict[key] = cal_list

        if skip_sun != 0:
            weekday = 6
        if skip_sat != 0:
            weekday = 5

        for key in cd_dict:
            cal_list = []
            for cd in cd_frequency:
                if skip_sun != 0 or skip_sat != 0:
                    day_of_week = dt.datetime.strptime(cd_dict[key][int(cd) - 1], '%Y-%m-%d')
                    if (dt.date.weekday(day_of_week)) == weekday:
                        skip_back_sun = skip_sun - 1
                        cal_list.append(cd_dict[key][int(cd) + skip_back_sun])
                    else:
                        cal_list.append(cd_dict[key][int(cd) - 1])
                else:
                    cal_list.append(cd_dict[key][int(cd) - 1])

            c_cal_dict[key] = cal_list

        combined_cal_dict = {key: w_cal_dict[key] + c_cal_dict[key] for key in w_cal_dict}

        return combined_cal_dict

    #################################################################
    # function to derive WEEK days based on specific calendar logic

    def calc_weekdays(start_dt, offset, skip_frequency):
        wk_dict = {}
        for dt_range in pd.date_range(start=start_dt, periods=12, freq='MS'):
            end_dt_list = pd.date_range(start=dt_range, periods=1, freq='M').strftime("%Y-%m-%d")
            month_start_dt = dt_range.strftime("%Y-%m-%d")
            month_end_dt = end_dt_list.values[0]
            wk_list = []
            for wk_dt in pd.date_range(month_start_dt, month_end_dt, freq=offset):
                get_wk_dt = wk_dt.strftime("%Y-%m-%d")
                wk_list.append(get_wk_dt)

            period_name = dt.datetime.strptime(month_start_dt, "%Y-%m-%d")
            period_name_month = period_name.strftime('%b')
            period_name_yr = period_name.strftime('%y')
            period_key = f'{period_name_month}-{period_name_yr}'

            if skip_frequency > 0:
                wk_len = len(wk_list)
                wk_slice = slice(0, wk_len, (skip_frequency+1))
                wk_dict[period_key] = wk_list[wk_slice]
            else:
                wk_dict[period_key] = wk_list

        return wk_dict

    #################################################################

    # read calendar definition based on calendar names in the file
    cal_data = pd.read_csv("definitions/calendar_data.csv", na_values='null', keep_default_na=False)

    names_list = cal_data.columns.values.tolist()
    names_list.pop(0)

    calendar_dict = {}
    for name in names_list:

        if cal_data[name][0] == 'work_days':
            list_of_wd = (cal_data[name][1]).split(',')
            skip_wd = (cal_data[name][2]).split(',')
            calendar_dict[name] = calc_wd_dates(list_of_wd, skip_wd)
        elif cal_data[name][0] == 'calendar_days':
            list_of_cd = (cal_data[name][3]).split(',')
            move_sat = cal_data[name][4]
            move_sun = cal_data[name][5]
            calendar_dict[name] = calc_cd_dates(list_of_cd, int(move_sat), int(move_sun))
        elif cal_data[name][0] == 'both_days':
            list_of_wd = (cal_data[name][1]).split(',')
            # skip_wd = (cal_data[name][2]).split(',')
            list_of_cd = (cal_data[name][3]).split(',')
            move_sat = cal_data[name][4]
            move_sun = cal_data[name][5]
            calendar_dict[name] = calc_both_days(list_of_wd, list_of_cd, int(move_sat), int(move_sun))
        elif cal_data[name][0] == 'weekdays':
            runs_weekly = (cal_data[name][6])
            skip_range = (cal_data[name][7])
            calendar_dict[name] = calc_weekdays(v_start_date, runs_weekly, int(skip_range))

    return calendar_dict


# Create a Custom Calendar Object using Custom holiday list
try:
    holiday_data = pd.read_csv('definitions/HolidayList.csv')
except FileNotFoundError as err_msg:
    print(f'{err_msg} - Did you forget something?')
else:
    rows = holiday_data.iterrows()
    holiday_list = [row[1]['Holiday'] for row in rows]
    v_year = holiday_list[0][0:4]

    try:
        for date in holiday_list:
            if date[0:4] != v_year:
                raise ValueError("Holiday Calendar contains multiple year!!")
    except ValueError as err_msg:
        print(err_msg)
    else:
        cal_dict = generate_cal_f(holiday_list)
        #print(cal_dict)
        # Create a calendar data frame
        cal_df = {}
        cal_df_dict = {}
        for key in cal_dict:
            cal_list = []
            chain_list = []
            cal_df_dict = cal_dict[key]
            # print(cal_df_dict)
            for values in cal_df_dict.values():
                # print(values)
                cal_list.append(values)

            chain_list = list(itertools.chain.from_iterable(cal_list))
            cal_df[key] = chain_list

        #print(cal_df)

        # write dataframe to Excel file
        df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in cal_df.items()]))
        df.to_excel("output/CALENDAR.xlsx", index=False)