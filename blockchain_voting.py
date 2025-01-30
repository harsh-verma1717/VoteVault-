import hashlib
import time
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class Block:
    def __init__(self, index, voter_id, candidate, previous_hash):
        self.index = index
        self.voter_id = voter_id
        self.candidate = candidate
        self.timestamp = time.time()
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.voter_id}{self.candidate}{self.timestamp}{self.previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "Genesis", "None", "0")

    def add_vote(self, voter_id, candidate):
        previous_block = self.chain[-1]
        new_block = Block(len(self.chain), voter_id, candidate, previous_block.hash)
        self.chain.append(new_block)

class VotingApp:
    def __init__(self, root, blockchain):
        self.root = root
        self.blockchain = blockchain
        self.voter_ids = set()
        self.vote_counts = {candidate: 0 for candidate in ["Modi", "Trump", "Putin", "Kim Jong","Harsh"]}
        self.valid_voter_ids = {f"V{i}" for i in range(1, 21)}
        self.root.title("Blockchain Voting System")
        self.root.geometry("800x600")
        self.root.config(bg="#0f0f0f")

        self.header_label = tk.Label(
            self.root,
            text="BLOCKCHAIN VOTING SYSTEM",
            font=("Arial", 18, "bold"),
            bg="#0f0f0f",
            fg="#00ff00"
        )
        self.header_label.pack(pady=10)
        input_frame = tk.Frame(self.root, bg="#0f0f0f", pady=10)
        input_frame.pack()

        self.voter_id_label = tk.Label(input_frame, text="Enter Voter ID:", font=("Arial", 14), bg="#0f0f0f", fg="#00ff00")
        self.voter_id_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.voter_id_entry = tk.Entry(input_frame, font=("Arial", 14), bg="#1e1e1e", fg="#00ff00", insertbackground="#00ff00")
        self.voter_id_entry.grid(row=0, column=1, padx=10, pady=5)

        self.candidate_label = tk.Label(input_frame, text="Select Candidate:", font=("Arial", 14), bg="#0f0f0f", fg="#00ff00")
        self.candidate_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.candidates = list(self.vote_counts.keys())
        self.candidate_var = tk.StringVar()
        self.candidate_var.set(self.candidates[0])
        self.candidate_menu = tk.OptionMenu(input_frame, self.candidate_var, *self.candidates)
        self.candidate_menu.config(font=("Arial", 14), bg="#1e1e1e", fg="#00ff00", activebackground="#00ff00", activeforeground="#0f0f0f")
        self.candidate_menu["menu"].config(bg="#1e1e1e", fg="#00ff00")
        self.candidate_menu.grid(row=1, column=1, padx=10, pady=5)

        self.submit_vote_button = tk.Button(
            self.root,
            text="SUBMIT VOTE",
            font=("Arial", 14, "bold"),
            bg="#00ff00",
            fg="#0f0f0f",
            command=self.submit_vote
        )
        self.submit_vote_button.pack(pady=20)

        self.blockchain_label = tk.Label(
            self.root,
            text="BLOCKCHAIN RECORDS:",
            font=("Arial", 14, "bold"),
            bg="#0f0f0f",
            fg="#00ff00"
        )
        self.blockchain_label.pack(anchor="w", padx=20)
        self.blockchain_text = tk.Text(
            self.root,
            wrap=tk.WORD,
            font=("Arial", 12),
            width=90,
            height=15,
            bg="#1e1e1e",
            fg="#00ff00",
            insertbackground="#00ff00"
        )
        self.blockchain_text.pack(padx=20, pady=10)
        self.blockchain_text.config(state=tk.DISABLED)

        self.update_blockchain_display()

    def submit_vote(self):
        voter_id = self.voter_id_entry.get()
        candidate = self.candidate_var.get()

        if voter_id not in self.valid_voter_ids:
            messagebox.showerror("Invalid Voter ID", "This voter ID is not authorized.")
            return
        elif voter_id in self.voter_ids:
            messagebox.showerror("Duplicate Vote", "This voter ID has already been used.")
        else:
            self.blockchain.add_vote(voter_id, candidate)
            self.voter_ids.add(voter_id)
            self.vote_counts[candidate] += 1
            self.update_blockchain_display()

            if self.vote_counts[candidate] >= 3:
                self.display_results(candidate)
                self.submit_vote_button.config(state=tk.DISABLED)

            messagebox.showinfo("Vote Submitted", f"Vote for {candidate} submitted!")
            self.voter_id_entry.delete(0, tk.END)
        
    def update_blockchain_display(self):
        self.blockchain_text.config(state=tk.NORMAL)
        self.blockchain_text.delete(1.0, tk.END)
        for block in self.blockchain.chain:
            readable_time = datetime.fromtimestamp(block.timestamp).strftime("%d-%m-%Y %H:%M:%S")
        
            block_info = (
                f"Index: {block.index}\n"
                f"Voter ID: {block.voter_id}\n"
                f"Candidate: {block.candidate}\n"
                f"Timestamp: {readable_time}\n" 
                f"Previous Hash: {block.previous_hash}\n"
                f"Hash: {block.hash}\n\n"
            )
            self.blockchain_text.insert(tk.END, block_info)
        self.blockchain_text.config(state=tk.DISABLED)


    def display_results(self, winner):
        results_window = tk.Toplevel(self.root)
        results_window.title("ELECTION RESULTS")
        results_window.geometry("400x300")
        results_window.config(bg="#0f0f0f")

        winner_label = tk.Label(
            results_window,
            text=f"🏆 WINNER: {winner} 🏆",
            font=("Arial", 16, "bold"),
            bg="#0f0f0f",
            fg="#00ff00"
        )
        winner_label.pack(pady=20)

        tally_label = tk.Label(results_window, text="FINAL TALLY:", font=("Arial", 14), bg="#0f0f0f", fg="#00ff00")
        tally_label.pack()

        tally_text = tk.Text(
            results_window,
            font=("Arial", 12),
            bg="#1e1e1e",
            fg="#00ff00",
            height=10,
            width=40
        )
        tally_text.pack(pady=10)
        tally_text.insert(tk.END, "\n".join([f"{candidate}: {count} votes" for candidate, count in self.vote_counts.items()]))
        tally_text.config(state=tk.DISABLED)

        close_button = tk.Button(
            results_window,
            text="CLOSE",
            font=("Arial", 12, "bold"),
            bg="#00ff00",
            fg="#0f0f0f",
            command=results_window.destroy
        )
        close_button.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    blockchain = Blockchain()
    app = VotingApp(root, blockchain)
    root.mainloop()
