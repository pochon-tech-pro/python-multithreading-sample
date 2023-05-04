import requests
import threading
import time
import multiprocessing

# ウェブページのリスト
urls = [
    "https://www.example.com",
    "https://www.example.org",
    "https://www.example.net",
    "https://www.example.co.uk",
    "https://www.example.com",
    "https://www.example.org",
    "https://www.example.net",
    "https://www.example.co.uk",
]


# ウェブページをダウンロードする関数
def download_page(url):
    # time.sleep(1)
    requests.get(url)


# シングルスレッドでウェブページをダウンロード
def single_threaded():
    for url in urls:
        download_page(url)


# マルチスレッドでウェブページをダウンロード
def multi_threaded():
    threads = []
    for url in urls:
        t = threading.Thread(target=download_page, args=(url,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()


# シングルスレッド・マルチプロセスでウェブページをダウンロード
def single_threaded_multi_process():
    with multiprocessing.Pool() as pool:
        pool.map(download_page, urls)


def worker(url_list):
    threads = []
    for url in url_list:
        t = threading.Thread(target=download_page, args=(url,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()


# マルチスレッド・マルチプロセスでウェブページをダウンロード
def multi_threaded_multi_process():
    chunked_urls = [urls[i::2] for i in range(2)]  # Split urls into 2 chunks
    with multiprocessing.Pool(2) as pool:
        pool.map(worker, chunked_urls)


if __name__ == "__main__":
    start_time_single = time.time()
    single_threaded()
    end_time_single = time.time()
    time_taken_single = end_time_single - start_time_single
    print(f"処理時間 (single-threaded, single-process): {time_taken_single} seconds")

    start_time_multi = time.time()
    multi_threaded()
    end_time_multi = time.time()
    time_taken_multi = end_time_multi - start_time_multi
    print(f"処理時間 (multi-threaded, single-process): {time_taken_multi} seconds")

    start_time_mp = time.time()
    single_threaded_multi_process()
    end_time_mp = time.time()
    time_taken_mp = end_time_mp - start_time_mp
    print(f"処理時間 (single-threaded, multi-process): {time_taken_mp} seconds")

    start_time_mtmp = time.time()
    multi_threaded_multi_process()
    end_time_mtmp = time.time()
    time_taken_mtmp = end_time_mtmp - start_time_mtmp
    print(f"処理時間 (multi-threaded, multi-process): {time_taken_mtmp} seconds")
