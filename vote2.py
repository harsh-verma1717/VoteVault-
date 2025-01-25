import hashlib
import time
import tkinter as tk
from tkinter import messagebox

class Block:
    def __init__(self, index, voter_id, candidate, previous_hash):
        self.index = index
        self.voter_id = voter_id
        self.candidate = candidate
        self.timestamp = time.time()
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_data = f"{self.index}{self.voter_id}{self.candidate}{self.timestamp}{self.previous_hash}"
        return hashlib.sha256(block_data.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "Genesis", "None", "0")

    def add_vote(self, voter_id, candidate):
        prev_block = self.chain[-1]
        new_block = Block(len(self.chain), voter_id, candidate, prev_block.hash)
        self.chain.append(new_block)

class VotingApp:
    def __init__(self, root, blockchain):
        self.root = root
        self.blockchain = blockchain
        self.voter_ids = set()
        self.vote_counts = {c: 0 for c in ["Nakshatra", "Rudra", "Thakur", "Pratham", "Gurprit", "Harsh"]}
        self.valid_voter_ids = {f"V{i}" for i in range(1, 11)}
        self.root.title("Voting System")
        self.root.geometry("800x600")
        self.root.config(bg="#0f0f0f")

        tk.Label(self.root, text="BLOCKCHAIN VOTING SYSTEM", font=("Arial", 18, "bold"), bg="#0f0f0f", fg="#00ff00").pack(pady=10)

        input_frame = tk.Frame(self.root, bg="#0f0f0f")
        input_frame.pack()

        tk.Label(input_frame, text="Voter ID:", font=("Arial", 14), bg="#0f0f0f", fg="#00ff00").grid(row=0, column=0, padx=10, pady=5)
        self.voter_id_entry = tk.Entry(input_frame, font=("Arial", 14), bg="#1e1e1e", fg="#00ff00")
        self.voter_id_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(input_frame, text="Candidate:", font=("Arial", 14), bg="#0f0f0f", fg="#00ff00").grid(row=1, column=0, padx=10, pady=5)
        self.candidate_var = tk.StringVar(value=list(self.vote_counts.keys())[0])
        tk.OptionMenu(input_frame, self.candidate_var, *self.vote_counts.keys()).grid(row=1, column=1, padx=10, pady=5)

        tk.Button(self.root, text="SUBMIT VOTE", font=("Arial", 14), bg="#00ff00", command=self.submit_vote).pack(pady=20)

        tk.Label(self.root, text="BLOCKCHAIN RECORDS:", font=("Arial", 14), bg="#0f0f0f", fg="#00ff00").pack(anchor="w", padx=20)
        self.blockchain_text = tk.Text(self.root, wrap=tk.WORD, font=("Arial", 12), width=90, height=15, bg="#1e1e1e", fg="#00ff00", state=tk.DISABLED)
        self.blockchain_text.pack(padx=20, pady=10)

        self.update_blockchain_display()

    def submit_vote(self):
        voter_id = self.voter_id_entry.get()
        candidate = self.candidate_var.get()

        if voter_id not in self.valid_voter_ids:
            messagebox.showerror("Error", "Invalid Voter ID.")
        elif voter_id in self.voter_ids:
            messagebox.showerror("Error", "Vote already submitted.")
        else:
            self.blockchain.add_vote(voter_id, candidate)
            self.voter_ids.add(voter_id)
            self.vote_counts[candidate] += 1
            self.update_blockchain_display()

            if self.vote_counts[candidate] >= 3:
                self.show_results(candidate)
                return

            messagebox.showinfo("Success", f"Vote for {candidate} submitted!")
            self.voter_id_entry.delete(0, tk.END)

    def update_blockchain_display(self):
        self.blockchain_text.config(state=tk.NORMAL)
        self.blockchain_text.delete(1.0, tk.END)
        for block in self.blockchain.chain:
            self.blockchain_text.insert(tk.END, f"Index: {block.index}\nVoter ID: {block.voter_id}\nCandidate: {block.candidate}\nHash: {block.hash}\n\n")
        self.blockchain_text.config(state=tk.DISABLED)

    def show_results(self, winner):
        result_window = tk.Toplevel(self.root)
        result_window.title("Results")
        result_window.geometry("400x300")
        result_window.config(bg="#0f0f0f")

        tk.Label(result_window, text=f"WINNER: {winner}", font=("Arial", 16), bg="#0f0f0f", fg="#00ff00").pack(pady=20)
        tk.Label(result_window, text="FINAL TALLY:", font=("Arial", 14), bg="#0f0f0f", fg="#00ff00").pack()
        tally_text = tk.Text(result_window, font=("Arial", 12), bg="#1e1e1e", fg="#00ff00", height=10, width=40)
        tally_text.pack(pady=10)
        for candidate, count in self.vote_counts.items():
            tally_text.insert(tk.END, f"{candidate}: {count} votes\n")
        tally_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    blockchain = Blockchain()
    VotingApp(root, blockchain)
    root.mainloop()
