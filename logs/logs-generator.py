import faker
from datetime import datetime, timedelta
import random
from constant import Constant

def generate_datetime(start_date:datetime,end_date:datetime,nb_logs:int)->list[datetime]:
    """
    Générer des timestamps aléatoires entre deux dates

    """
    timestamps = []
    total_seconds = (end_date -start_date).total_seconds()
    for _ in range(nb_logs): 
        random_offset = random.random() * total_seconds
        timestamp = start_date + timedelta(seconds=random_offset)
        formatted_timestamp=timestamp.strftime('%Y-%m-%d %H:%M:%S')
        timestamps.append(formatted_timestamp)
        timestamps.sort()
    return timestamps
    

def generate_anomaly_intervals(
        number_of_anomaly_intervals:int,
        number_of_logs:int,
        max_number_of_anomaly_per_interval:int,
        min_number_of_anomaly_per_interval:int,
        anomaly_types:list[str]
)->list[dict[str,int|str]]:
    
    """
    Générer les intervalles d'anomalies

    """

    intervals = []
    for _ in range(number_of_anomaly_intervals):
        start_idx = random.randint(0,number_of_logs - max_number_of_anomaly_per_interval -1)
        nb_anomaly = random.randint(min_number_of_anomaly_per_interval,max_number_of_anomaly_per_interval)
        end_idx = min(start_idx + nb_anomaly, number_of_logs -1)
        intervals.append({
            "start_idx": start_idx,
            "end_idx": end_idx,
            "type": random.choice(anomaly_types) 
        })
    return intervals


def generate_logs_dataset(
        start_date:datetime,
        end_date:datetime,
        nb_logs:int,
        number_of_anomaly_intervals:int,
        max_number_of_anomaly_per_interval:int,
        min_number_of_anomaly_per_interval:int,
        number_of_anomaly_ips:int,
        http_methods:list[str],
        http_normal_code:list[str],
        http_error_code:dict[str,list[str]],
        http_error_list:list[str],
        api_endpoints:list[str],
        logs_dataset_file_name:str
):
    """
    Générer un dataset de logs avec des anomalies

    """
    fak = faker.Faker()
    anomaly_ips = [fak.ipv4() for _ in range(number_of_anomaly_ips)]
    timestamps = generate_datetime(
        start_date=start_date,
        end_date=end_date,
        nb_logs=nb_logs
    )
    anomaly_types = http_error_list.copy()
    anomaly_types.append("mixed errors")
    anomaly_intervals = generate_anomaly_intervals(
        number_of_anomaly_intervals=number_of_anomaly_intervals,
        number_of_logs=nb_logs,
        max_number_of_anomaly_per_interval=max_number_of_anomaly_per_interval,
        min_number_of_anomaly_per_interval=min_number_of_anomaly_per_interval,
        anomaly_types=anomaly_types
    )
    
    with open(logs_dataset_file_name,"w") as file:
        
        file.write("timestamp,user_ip,method,status_code,end_point,response_time\n")

        for i in range(nb_logs):
            timestamp = timestamps[i]
            user_ip = fak.ipv4()
            method = random.choice(http_methods)
            status_code = random.choice(http_normal_code)
            end_point= random.choice(api_endpoints)
            response_time = random.randint(0,300)

            for interval in anomaly_intervals:
                if interval["start_idx"] <= i <= interval["end_idx"]:
                    user_ip = random.choice(anomaly_ips)
                    if interval["type"] == "server_errors":
                        status_code = random.choice(http_error_code["server_errors"])
                    elif interval["type"] == "client_errors":
                        status_code = random.choice(http_error_code["client_errors"])
                    elif interval["type"] == "timeout_errors":
                        status_code = random.choice(http_error_code["timeout_errors"])  
                        response_time = random.randint(1000,5000)
                    else:
                        status_code = random.choice(list(http_error_code.values())[0])
                        response_time = random.randint(1000,5000)
            file.write(f"{timestamp},{user_ip},{method},{status_code},{end_point},{response_time}\n")
    print(f"[OK] Le fichier CSV '{logs_dataset_file_name}' a été généré avec {nb_logs} logs et {number_of_anomaly_intervals} plage d'anomalies.")

if __name__ == "__main__":
    generate_logs_dataset(
        start_date = Constant.LOG_START_DATE,
        end_date= Constant.LOG_END_DATE,
        nb_logs= Constant.NB_LOGS,
        number_of_anomaly_intervals= Constant.NUMBER_OF_ANOMALY_INTERVALS,
        max_number_of_anomaly_per_interval= Constant.MAX_NUMBER_OF_ANOMALY_PER_INTERVAL,
        min_number_of_anomaly_per_interval= Constant.MIN_NUMBER_OF_ANOMALY_PER_INTERVAL,
        number_of_anomaly_ips= Constant.NUMBER_OF_ANOMAMLY_IPS,
        http_methods= Constant.HTTP_METHODS,
        http_normal_code= Constant.HTTP_NORMAL_CODES,
        http_error_code= Constant.HTTP_ERROR_CODES,
        http_error_list=list(Constant.HTTP_ERROR_CODES.keys()),
        api_endpoints= Constant.API_ENDPOINTS,
        logs_dataset_file_name= Constant.LOGS_DATA_FILE_NAME
    )