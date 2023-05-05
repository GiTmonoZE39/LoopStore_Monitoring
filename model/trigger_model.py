import mysql.connector
from datetime import datetime, timedelta
from pytz import timezone

class TriggerModel:
    #constructor below
    def __init__(self):
        #connection establishment code (b/w python & mySQL)
        try:
            self.con = mysql.connector.connect(host="localhost", user="root", password="MySQL@pass123", database="loopstore")
            self.cur = self.con.cursor(dictionary=True) #retrieve data in dict format
            print("Connection Successful")
        except:
            print("Some error")

    def trigger_model_method(self):
        #Query execution code
        self.cur.execute("SELECT storestatus.store_id, storestatus.status, storestatus.timestamp_utc, timezone.timezone_str, businesshours.day, businesshours.start_time_local, businesshours.end_time_local FROM storestatus INNER JOIN timezone ON storestatus.store_id = timezone.store_id INNER JOIN businesshours ON storestatus.store_id = businesshours.store_id")

        result = self.cur.fetchall()
        final_data = {}

        #Loop through the result of the query and perform necessary calculations
        for row in result:
            store_id = row['store_id']
            status = row['status']
            timezone_str = row['timezone_str']
            day = row['day']
            start_time_local = row['start_time_local']
            end_time_local = row['end_time_local']
            timestamp_utc = row['timestamp_utc']

            #Convert the timezone string to a timezone object
            tz = timezone(timezone_str)

            #Convert the timestamp_utc to datetime object with timezone information
            timestamp_utc = datetime.strptime(timestamp_utc, "%Y-%m-%d %H:%M:%S")
            timestamp_utc = timezone('UTC').localize(timestamp_utc)

            #Convert the timestamp_utc to the timezone of the store
            timestamp_local = timestamp_utc.astimezone(tz)

            #Calculate the current datetime with timezone information
            now = datetime.now(tz)

            #If the status is active, calculate the uptime, otherwise calculate the downtime
            if status == 'active':
                #Calculate the uptime for the last hour
                last_hour_start = now - timedelta(hours=1)
                last_hour_start = last_hour_start.replace(minute=0, second=0, microsecond=0)
                if last_hour_start < timestamp_local:
                    uptime_last_hour = (now - timestamp_local).total_seconds() / 60
                else:
                    uptime_last_hour = 0

                #Calculate the uptime for the last day
                last_day_start = now - timedelta(days=1)
                last_day_start = last_day_start.replace(hour=0, minute=0, second=0, microsecond=0)
                if last_day_start < timestamp_local:
                    uptime_last_day = (now - timestamp_local).total_seconds() / 3600
                else:
                    uptime_last_day = 0

                #Calculate the uptime for the last week
                last_week_start = now - timedelta(weeks=1)
                last_week_start = last_week_start.replace(hour=0, minute=0, second=0, microsecond=0)
                if last_week_start < timestamp_local:
                    uptime_last_week = (now - timestamp_local).total_seconds() / 3600
                else:
                    uptime_last_week = 0

                #Set downtime values to 0 since the status is active
                downtime_last_hour = 0
                downtime_last_day = 0

            else:
              #Calculate the downtime for the last hour
              last_hour_start = now - timedelta(hours=1)
              last_hour_start = last_hour_start.replace(minute=0, second=0, microsecond=0)
              if last_hour_start < timestamp_local:
               downtime_last_hour = 60 - (now - timestamp_local).total_seconds() / 60
              else:
                downtime_last_hour = 60

             #Calculate the downtime for the last day
            last_day_start = now - timedelta(days=1)
            last_day_start = last_day_start.replace(hour=0, minute=0, second=0, microsecond=0)
            if last_day_start < timestamp_local:
              downtime_last_day = 24 - (now - timestamp_local).total_seconds() / 3600
            else:
                downtime_last_day = 24

            #Calculate the downtime for the last week
            last_week_start = now - timedelta(weeks=1)
            last_week_start = last_week_start.replace(hour=0, minute=0, second=0, microsecond=0)
            if last_week_start < timestamp_local:
             downtime_last_week = 168 - (now - timestamp_local).total_seconds() / 3600
            else:
             downtime_last_week = 168