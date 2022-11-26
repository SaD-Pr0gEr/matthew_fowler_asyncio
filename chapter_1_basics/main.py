# import requests
#
# response = requests.get('https://www.google.com')  # IO-bound
# items = response.headers.items()
# headers = [f'#{key}: {header}' for key, header in items]  # CPU-bound
# formatted_headers = '\n'.join(headers)  # CPU-bound


# with open("some_file.txt", "w", encoding="utf-8") as file:
#     file.write("some content")  # IO-bound

# import os
# import threading
# print(f'Исполняется Python-процесс с идентификатором: {os.getpid()}')
# total_threads = threading.active_count()
# thread_name = threading.current_thread().name
# print(f'В данный момент Python исполняет {total_threads} поток(ов)')
# print(f'Имя текущего потока {thread_name}')

# import threading
#
#
# def hello_from_thread():
#     print(f'Привет от потока {threading.current_thread()}!')
#
#
# hello_thread = threading.Thread(target=hello_from_thread)
# hello_thread.start()
# total_threads = threading.active_count()
# thread_name = threading.current_thread().name
# print(f'В данный момент Python выполняет {total_threads} поток(ов)')
# print(f'Имя текущего потока {thread_name}')
# hello_thread.join()


# import multiprocessing
# import os
#
#
# def hello_from_process():
#     print(f'Привет от дочернего процесса {os.getpid()}!')
#
#
# if __name__ == '__main__':
#     hello_process = multiprocessing.Process(target=hello_from_process)
#     hello_process.start()
#     print(f'Привет от родительского процесса {os.getpid()}')
#     hello_process.join()


# import time
#
#
# def print_fib(number: int) -> None:
#     def fib(n: int) -> int:
#         if n == 1:
#             return 0
#         elif n == 2:
#             return 1
#         else:
#             return fib(n - 1) + fib(n - 2)
#
#     print(f'fib({number}) равно {fib(number)}')
#
#
# def fibs_with_threads():
#     fortieth_thread = threading.Thread(target=print_fib, args=(40,))
#     forty_first_thread = threading.Thread(target=print_fib, args=(41,))
#     fortieth_thread.start()
#     forty_first_thread.start()
#     fortieth_thread.join()
#     forty_first_thread.join()
#
#
# start_threads = time.time()
# fibs_with_threads()
# end_threads = time.time()
# print(f'Время работы {end_threads - start_threads:.4f} с.')
