import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
# import seaborn as sns
import math
import datetime as dt
from flask import *

calculations_page = Blueprint('calculations_page', __name__)

@calculations_page.route('/compute_sampling_schedule', methods=['POST', 'GET'])
def compute_sampling_schedule():
    if request.method == 'POST':
        comp_dict = {}

        pct_dict = {'1': np.arange(0, 130, 10)}

        for item, val in request.form.items():
            comp_dict[item] = val

        # Probably a better way to do this
        for i in ['capacity', 'flow_rate']:
            comp_dict[i] = float(comp_dict[i])
        comp_dict['sample_pcts'] = pct_dict[comp_dict['sample_pcts']]

        print(comp_dict)

        if comp_dict['system_type'] == 'plumbed':
            # javascript to add in cycle info
            start_time = ' '.join([comp_dict['start_date'], comp_dict['start_time']])

            df = gen_dataframe(on_mins=int(comp_dict['on_mins']), off_mins=int(comp_dict['off_mins']), flow_rate=comp_dict['flow_rate'], capacity=comp_dict['capacity'], sample_pcts=comp_dict['sample_pcts'], start_time = start_time)

        elif comp_dict['system_type'] == 'pour':
            # javascript to add in batch size
            df = gen_pour_df(batch_size=comp_dict['batch_size'], flow_rate=comp_dict['flow_rate'], capacity=comp_dict['capacity'], sample_pcts=[0, 25, 50, 75, 100, 150, 180, 200])

        json_df = df.to_json(orient='records')

        sampling_table = df[df.sampling_point][['vol_passed', 'pct_capacity', 'test_day', 'hours_into_day', 'dt']]
        # Formatting for table
        sampling_table.pct_capacity = sampling_table.pct_capacity.round()
        sampling_table.test_day = sampling_table.test_day.astype('int32')
        sampling_table.dt = sampling_table.dt.dt.round('1min').astype('<M8[m]')
        sampling_table.hours_into_day = pd.to_datetime(sampling_table.hours_into_day, unit='h').dt.round('1min').astype('M8[m]').dt.time
        sampling_table.columns = ['Total Volume', '% Capacity', 'Test Day', 'Time Into Day (H:M)', 'Expected Date']

        return render_template('compute_sampling_schedule.html', sampling_table = sampling_table.to_html(index = 0), json_df = json_df)

    return render_template('compute_sampling_schedule.html')



def gen_increase_array(on_mins, off_mins, flow_rate):
    """
    Generates an array of a cycle, [0] is minutes, [1] is flow rate
    """
    cycle_time = on_mins + off_mins
    increase_array = []
    for i in range(on_mins):
        increase_array.append((1, flow_rate))
    for i in range(on_mins, cycle_time):
        increase_array.append((1, 0))
    return(increase_array)


def total_vol_time_run(increase_array, max_volume):
    increase_per_cycle = np.max(np.cumsum(increase_array, axis=0)[:,1])

    num_cycles = int(np.ceil(max_volume / increase_per_cycle))

    time_to_vol = np.cumsum(np.tile(increase_array, (num_cycles,1)), axis=0)
    return(time_to_vol)


def gen_collection_points(capacity):
    percentages = np.arange(0, 130, 10)
    return(capacity * percentages / 100)


def gen_dataframe(on_mins, off_mins, flow_rate, capacity, sample_pcts,
                  start_time):
    increase_array = gen_increase_array(on_mins, off_mins, flow_rate)
    collection_points = gen_collection_points(capacity)
    max_volume = collection_points[-1]
    time_to_vol = total_vol_time_run(increase_array, max_volume)
    frac_on = on_mins / (off_mins + on_mins)


    df = pd.DataFrame(time_to_vol)
    df.columns = ['cum_mins_running', 'vol_passed']
    df['pct_capacity'] = 100 * df.vol_passed / capacity
    df['test_day'] = np.ceil(df.vol_passed * (1 / flow_rate) * (1 / frac_on) / (16 * 60) )
    df['hours_into_day'] = (df.cum_mins_running / 60) % 16
    df.loc[df.hours_into_day == 0, 'hours_into_day'] = 16.0

    start_time = pd.to_datetime(start_time, format = '%Y-%m-%d %H:%M')
    df['dt'] = start_time + pd.to_timedelta(df.hours_into_day, unit = 'h') + pd.to_timedelta(df.test_day - 1, unit = 'd')
    #TODO: do aove with datetime
    # Collection column, boolean with idxmax and loc
    df['sampling_point'] = False

    def mark_collections():
        min_increment = np.min(df.pct_capacity)
        pcts_low = sample_pcts - min_increment
        pcts_high = sample_pcts + min_increment

        sampling_rows = []

        for i in range(len(sample_pcts)):
            sampling_row = df.loc[(np.where(np.logical_and(df.pct_capacity >= pcts_low[i], df.pct_capacity <= pcts_high[i])))].head(1)
            sampling_rows.append(sampling_row)

        sampling_rows = pd.concat(sampling_rows)
        sampling_rows['sampling_point'] = True

        df.update(sampling_rows)
        return(sampling_rows)


    mark_collections()

    return(df)


# def plot_with_markers(time_to_vol, collection_vols):
#     x, y = time_to_vol.T
#     plt.plot(x / 60, y, color = 'orange')

#     collection_vols = gen_collection_points(1665)
#     collection_points = []
#     for vol in collection_vols:
#         collection_points.append(
#             time_to_vol[np.logical_and(y >= vol - 1.25, y <= vol + 1.25)][0])

#     col_points = np.vstack(collection_points).T
#     print(col_points)
#     x, y = col_points
#     plt.scatter(x / 60, y, color = 'red')

#     for i in col_points.T:
#         mins, hours = math.modf((i[0] / 60) % 16)
#         hours = int(hours)
#         mins = int(mins * 60)
#         plt.text(x = i[0] / 60, y = i[1], s=f"Collect {hours}:{mins} after start")

#     plt.xlabel('Hours Running')
#     plt.ylabel('Volume Passed')

#     # Add a vertical line every 16 hours of running (1 day)
#     for i in range(10):
#         plt.axvline(x=i * 16)
#         plt.text(x = i * 16, y = np.max(y+10), s = f"Day {i+1}", rotation=90)

#     plt.show()

def pandas_plot(df):
    plt.plot('cum_mins_running', 'vol_passed',
             data = df)

    for i in range(1, 10):
        plt.axvline(x = i * 60 * 16)

    plt.show()


def radial_relative_plot(df):
    fig = plt.figure()
    for i in range(1, int(np.max(df.test_day)) + 1):
        day_df = df[df['test_day'] == i]
        ax = fig.add_subplot(2, 7, i, projection='polar')
        ax.plot(2 * np.pi * day_df['hours_into_day'] / 24,
                       day_df['pct_capacity'],
                alpha = 0.5)
        sampling_df = day_df[day_df.sampling_point == True]
        ax.bar(2 * np.pi * sampling_df['hours_into_day'] / 24,
                   # sampling_df['pct_capacity'],
                    np.max(df.pct_capacity),
               width = 0.1,
                   color = 'orange')
        ax.set_theta_direction(-1)
        ax.set_theta_zero_location('N')
        ax.set_xticklabels(["Day {}".format(i), '', '6', '', '12', '', '18'])
        ax.set_rmax(np.max(df.pct_capacity))
        # ax.set_title(f"Day {i}", pad = 1.0)
    plt.subplots_adjust(wspace = 0.7)
    plt.show()

def radial_real_plot(df):
    fig = plt.figure()
    start_date = min(df.dt.dt.date)
    start_weekday = (start_date.weekday() + 1) % 7 # shift 0 index to Sunday
    end_date = max(df.dt.dt.date)
    test_days = int(np.max(df.test_day))
    num_weeks = end_date.isocalendar()[1] - start_date.isocalendar()[1] + 1
    #TODO: resample to fill missing times with NaN
    for i in range(test_days):
        day_df = df[df.dt.dt.date == start_date + pd.Timedelta(i, unit = 'd')]
        # day_of_week = day_df.dt.dt.weekday.head(1)[0] # no permutation of this fucking works
        # day_of_week = i + 1
        day_of_week = start_weekday + i
        ax = fig.add_subplot(num_weeks, 7, day_of_week + 1, projection = 'polar')
        ax.plot(2 * np.pi * (day_df.dt.dt.hour + day_df.dt.dt.minute / 60) / 24,
                day_df.pct_capacity,
                alpha = 0.5)

        sampling_df = day_df[day_df.sampling_point == True]
        ax.bar(2 * np.pi * (sampling_df.dt.dt.hour + sampling_df.dt.dt.minute / 60 ) / 24,
                   # sampling_df['pct_capacity'],
                    np.max(df.pct_capacity),
               width = 0.1,
                   color = 'orange')

        ax.set_theta_direction(-1)
        ax.set_theta_zero_location('N')
        ax.set_xticklabels(['', '', '6', '', '12', '', '18', ''])
        ax.set_title("{}".format(start_date + pd.Timedelta(i, unit='d')))
        ax.set_rmax(np.max(df.pct_capacity))
    plt.subplots_adjust(wspace = 0.7)
    plt.show()

def gen_pour_df(batch_size, flow_rate, capacity, sample_pcts):
    batches_per_day = flow_rate / batch_size
    fill_events_per_day = np.ceil(batches_per_day)
    total_batches = math.ceil(capacity * sample_pcts[-1] * 0.01 / batch_size)
    fills_to_vol = []
    for i in range(1, total_batches + 1):
        fills_to_vol.append((i, i * batch_size))
    df = pd.DataFrame(fills_to_vol)
    df.columns = ['batch', 'vol_passed']

    df['pct_capacity'] = 100 * df.vol_passed / capacity
    df['test_day'] = np.ceil(df.batch / batches_per_day)

    df['batches_into_day'] = np.ceil(df.batch % (batches_per_day + 0.01))

    def mark_collections():
        df['sampling_point'] = False
        min_increment = np.min(df.pct_capacity)
        pcts_low = sample_pcts - min_increment
        pcts_high = sample_pcts + min_increment

        sampling_rows = []

        for i in range(len(sample_pcts)):
            sampling_row = df.loc[(np.where(np.logical_and(df.pct_capacity >= pcts_low[i], df.pct_capacity < pcts_high[i])))].tail(1)
            sampling_rows.append(sampling_row)

        sampling_rows = pd.concat(sampling_rows)
        sampling_rows['sampling_point'] = True

        df.update(sampling_rows)
    mark_collections()

    return(df)

#TODO: cast df as nx7 matrix to make a calendar

# # Generate the output of a stepwise function based on flow rate and  time on up to a max volume
# def gen_volume_at_cum_mins_array(max_vol, flow_rate, frac_on, num_filters=2):
#     total_minutes = max_vol / (flow_rate * frac_on)
