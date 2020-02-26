from main_loop import session

to_search = input("Stock to search for: ")
batch_size = input("Number of tweets to fetch at once (minimum 20): ")
wait_time = input("How long to wait after a successful fetch and analysis (in seconds): ")

session(to_search, batch_size, wait_time)
