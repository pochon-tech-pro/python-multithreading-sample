import csv
import threading
from collections import defaultdict
import time
import multiprocessing
import os

file_num = 3


# ログ解析関数
def analyze_log(args):
    file_name, output_file_name = args
    with open(file_name, "r") as f:
        reader = csv.reader(f)
        log_counter = defaultdict(int)
        for row in reader:
            _, process_name = row[0].split("-")
            log_counter[process_name] += 1

    with open(output_file_name, "w", newline="") as f:
        writer = csv.writer(f)
        for process_name, count in log_counter.items():
            writer.writerow([process_name, count])


# ログファイルの生成関数 (デモ用)
def create_log_file(file_name, num_rows):
    process_names = ["ProcessA", "ProcessB", "ProcessC"]
    with open(file_name, "w", newline="") as f:
        writer = csv.writer(f)
        for _ in range(num_rows):
            timestamp = int(time.time())
            process_name = process_names[_ % len(process_names)]
            writer.writerow([f"{timestamp}-{process_name}"])


def single_threaded():
    for i in range(file_num):
        analyze_log((log_files[i], f"output_single_threaded_{i}.csv"))


def multi_threaded():
    threads = []
    for i in range(file_num):
        t = threading.Thread(
            target=analyze_log, args=((log_files[i], f"output_multi_threaded_{i}.csv"),)
        )
        t.start()
        threads.append(t)

    for t in threads:
        t.join()


def multi_process():
    with multiprocessing.Pool() as pool:
        pool.map(
            analyze_log,
            [(log_files[i], f"output_multi_process_{i}.csv") for i in range(file_num)],
        )


if __name__ == "__main__":
    # デモ用ログファイルの生成
    log_files = [f"input_log_{i}.csv" for i in range(file_num)]
    for log_file in log_files:
        create_log_file(log_file, 1000000)

    # シングルスレッドでの処理時間計測
    start_time_single = time.time()
    single_threaded()
    end_time_single = time.time()
    result_time_single = end_time_single - start_time_single
    print(f"処理時間(single-threaded): {result_time_single} seconds")

    # マルチスレッドでの処理時間計測
    # GIL（同時に複数スレッドがPythonのオブジェクトへアクセスさせない仕組み）の影響でシングルスレッドよりも遅い場合がある
    # CPUバウンドな処理（CPUリソースを中心に使用する処理）の場合は、マルチプロセスの方が高速になる
    start_time_multi = time.time()
    multi_threaded()
    end_time_multi = time.time()
    result_time_multi = end_time_multi - start_time_multi
    print(f"処理時間(multi-threaded): {result_time_multi} seconds")

    # マルチプロセスでの処理時間計測
    start_time_mp = time.time()
    multi_process()
    end_time_mp = time.time()
    result_time_mp = end_time_mp - start_time_mp
    print(f"処理時間(multi-process): {result_time_mp} seconds")

    # ファイルを削除する
    for log_file in log_files:
        os.remove(log_file)
    for i in range(file_num):
        os.remove(f"output_single_threaded_{i}.csv")
        os.remove(f"output_multi_threaded_{i}.csv")
        os.remove(f"output_multi_process_{i}.csv")
