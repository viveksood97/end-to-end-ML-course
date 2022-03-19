import datetime
import requests

def downlaod_data(verbose=True):
    """
    Pull the data down from the public servers

    Args:
        verbose (bool, optional): _description_. Defaults to True.
    
    Returns:
        trips: list of dicts
    """
    harvard_stop_id = '70068'
    jfk_stop_id = '70086'

    start_time = datetime.time(7, 0)
    end_time = datetime.time(10, 0)

    start_date = datetime.date(2021, 12, 20)
    end_date = datetime.date(2022, 3, 19)

    TtravelURL = "http://realtime.mbta.com/developer/api/v2.1/traveltimes"
    TtravelKey = "?api_key=wX9NwuHnZU2ToO7GmGR9uw"
    Tformat = "&format=json"
    from_stop = "&from_stop=" + str(jfk_stop_id)
    to_stop = "&to_stop=" + str(harvard_stop_id)

    i_day = 0
    trips = []
    while True:
        check_date = start_date + datetime.timedelta(days=i_day)
        if check_date > end_date:
            break

        from_time = datetime.datetime.combine(check_date, start_time)
        to_time = datetime.datetime.combine(check_date, end_time)

        Tfrom_time = "&from_datetime=" + str(int(from_time.timestamp()))
        Tto_time = "&to_datetime=" + str(int(to_time.timestamp()))

        SRequest = "".join([
            TtravelURL,
            TtravelKey,
            Tformat,
            from_stop, to_stop,
            Tfrom_time, Tto_time
        ])

        s = requests.get(SRequest)
        s_json = s.json()
        for trip in s_json['travel_times']:
            trips.append({
                'dep': datetime.datetime.fromtimestamp(float(trip['dep_dt'])),
                'arr': datetime.datetime.fromtimestamp(float(trip['arr_dt']))
            })
        
        if(verbose):
            print(check_date, ':', len(s_json['travel_times']))
        
        i_day += 1

    return trips

if __name__ == '__main__':
    trips = downlaod_data()
