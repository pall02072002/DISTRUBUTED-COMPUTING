# Experiment 5: Implement Election Algorithm
# Bully Election Algorithm + Ring Election Algorithm

# ------------------ Bully Election ------------------
class BullyElection:
    def __init__(self, processes):
        self.processes = sorted(processes)
        self.alive = {p: True for p in processes}
        self.coordinator = max(processes)
        print(f"Initial Coordinator (Bully): {self.coordinator}")

    def crash(self, pid):
        if pid in self.alive:
            self.alive[pid] = False
            if pid == self.coordinator:
                print(f"\n[!] Coordinator Process {pid} has crashed.")
            else:
                print(f"\n[!] Process {pid} has crashed.")

    def start_election(self, pid):
        print(f"\n--- Election started by Process {pid} ---")

        higher_processes = [p for p in self.processes if p > pid]
        higher_alive = [p for p in higher_processes if self.alive[p]]

        if not higher_alive:
            self.coordinator = pid
            print(f"Process {pid}: No higher processes alive. I am the new Coordinator!")
        else:
            print(f"Process {pid} sends Election messages to: {higher_processes}")
            print(f"Alive higher processes: {higher_alive}")

            new_leader = max(higher_alive)
            self.start_election(new_leader)

    def show_coordinator(self):
        print(f"Current Coordinator (Bully): {self.coordinator}")


# ------------------ Ring Election ------------------
class RingElection:
    def __init__(self, processes):
        self.processes = sorted(processes)
        self.alive = {p: True for p in processes}
        self.coordinator = max(processes)
        print(f"\nInitial Coordinator (Ring): {self.coordinator}")

    def crash(self, pid):
        if pid in self.alive:
            self.alive[pid] = False
            print(f"\n[!] Process {pid} has crashed.")

    def start_election(self, starter):
        print(f"\n--- Process {starter} starts election ---")
        active_list = []
        n = len(self.processes)

        start_index = self.processes.index(starter)

        for i in range(n):
            current_pid = self.processes[(start_index + i) % n]
            if self.alive[current_pid]:
                active_list.append(current_pid)
                print(f"Process {current_pid} adds itself -> {active_list}")

        new_leader = max(active_list)
        self.coordinator = new_leader
        print(f"Election complete. New Coordinator: {new_leader}")

    def show_coordinator(self):
        print(f"Current Coordinator (Ring): {self.coordinator}")


# ------------------ MAIN ------------------
if __name__ == "__main__":

    print("===== Bully Election Algorithm =====")
    p_list1 = [1, 2, 3, 4, 5]
    bully = BullyElection(p_list1)

    bully.crash(5)          # Coordinator crashes
    bully.start_election(2) # Process 2 starts election
    bully.show_coordinator()

    print("\n===== Ring Election Algorithm =====")
    p_list2 = [1, 2, 3, 4]
    ring = RingElection(p_list2)

    ring.crash(4)           # Coordinator crashes
    ring.start_election(2)  # Process 2 starts election
    ring.show_coordinator()