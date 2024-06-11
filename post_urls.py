import requests
import pandas as pd


def post_url(url):
    endpoint = "http://127.0.0.1:8000/process_url/" 
    response = requests.post(endpoint, data={"url": url})
    if response.status_code == 200:
        response_json = response.json()
        print(f"Successfully processed URL: {url}, UUID: {response_json['uuid']}")
        return response_json
    else:
        print(f"Failed to process URL: {url}, Status Code: {response.status_code}, Error: {response.json()}")
        return None


def read_urls_from_csv(file_path):
    df = pd.read_csv(file_path)
    if 'url' not in df.columns:
        raise ValueError("CSV file must contain a 'url' column")
    return df['url'].tolist()



def post_urls_sequentially(urls):
    
    
    mysql_counter = 0
    redis_counter = 0
    cache_counter = 0
    
    
    for url in urls:
        response_json = post_url(url)
        if response_json:
            mysql_counter += response_json.get('elapsed_mysql_time', 0)
            redis_counter += response_json.get('elapsed_redis_time', 0)
            cache_counter += response_json.get('elapsed_cache_time', 0)
        
    print(f"Total mysql proccessing time = {mysql_counter}")
    print(f"Total redis proccessing time = {redis_counter}")
    print(f"Total cache proccessing time = {cache_counter}")
    
if __name__ == "__main__":
    #file_path = "/home/rafael/Desktop/url_uuid_v2/urls.csv"
    #file_path = "/home/rafael/Desktop/PyScripts/urls.csv"
    file_path = "/home/rafael/Downloads/urls.csv"
    urls = read_urls_from_csv(file_path)
    post_urls_sequentially(urls)


