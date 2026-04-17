# Experiment 6: Mutual Exclusion using Token Passing

import threading
import time
import random

class Process:
    def __init__(self, pid):
        self.pid = pid
        self.has_token = False
        self.request = False

    def request_cs(self):
        if not self.has_token:
            print(f"\n[!] Process {self.pid} requesting Critical Section")
            self.request = True

    def enter_cs(self):
        print(f" >>> Process {self.pid} ENTERED Critical Section")
        time.sleep(2)
        print(f" <<< Process {self.pid} EXITING Critical Section")
        self.request = False


def token_algorithm(processes):
    token_holder = 0
    processes[token_holder].has_token = True
    print(f"System Initialized: Process {token_holder} has the token")

    while True:
        current = processes[token_holder]

        # If current holder wants CS
        if current.request:
            current.enter_cs()

        # Check next requesting process
        for i in range(len(processes)):
            if processes[i].request and i != token_holder:
                print(f"Token Transfer: Process {token_holder} -> Process {i}")
                processes[token_holder].has_token = False
                processes[i].has_token = True
                token_holder = i
                break

        time.sleep(1)


# MAIN
if __name__ == "__main__":
    n = 3
    processes = [Process(i) for i in range(n)]

    def generate_requests():
        while True:
            time.sleep(random.randint(2, 5))
            p = random.choice(processes)
            p.request_cs()

    threading.Thread(target=token_algorithm, args=(processes,), daemon=True).start()
    threading.Thread(target=generate_requests, daemon=True).start()

    time.sleep(20)
    print("\nSimulation Finished")