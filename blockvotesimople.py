import hashlib
import time
import tkinter as tk
from tkinter import messagebox

# Define the Block class
class Block:
    def __init__(self, index, voter_id, candidate, previous_hash):
        self.index = index  # Position in the chain
        self.voter_id = voter_id  # Voter ID for the vote
        self.candidate = candidate  # Candidate voted for
        self.timestamp = time.time()  # When the vote was cast
        self.previous_hash = previous_hash  # Hash of the previous block
        self.hash = self.calculate_hash()  # Hash of this block

    def calculate_hash(self):
        # Combine all block information and hash it
        block_string = f"{self.index}{self.voter_id}{self.candidate}{self.timestamp}{self.previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()

# Define the Blockchain class
class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]  # Start with the genesis block

    def create_genesis_block(self):
        # Genesis block is the first block with no real data
        return Block(0, "Genesis", "None", "0")

    def add_vote(self, voter_id, candidate):
        # Create and add a new block to the chain
        previous_block = self.chain[-1]
        new_block = Block(len(self.chain), voter_id, candidate, previous_block.hash)
        self.chain.append(new_block)

# Define the VotingApp class for the GUI
class VotingApp:
    def __init__(self, root, blockchain):
        self.root = root
        self.blockchain = blockchain
        self.voter_ids_used = set()  # Keep track of voters who have voted
        self.vote_counts = {candidate: 0 for candidate in ["Alice", "Bob", "Charlie"]}  # Candidates and their votes
        self.valid_voter_ids = {f"V{i}" for i in range(1, 11)}  # Predefined valid voter IDs

        # Set up the GUI
        self.root.title("Simple Blockchain Voting System")
        self.root.geometry("800x600")
        self.root.config(bg="black")  # Dark background for hacker-style look

        # Header
        tk.Label(self.root, text="BLOCKCHAIN VOTING SYSTEM", font=("Arial", 18, "bold"), bg="black", fg="green").pack(pady=10)

        # Voter Input Section
        input_frame = tk.Frame(self.root, bg="black")
        input_frame.pack()

        tk.Label(input_frame, text="Enter Voter ID:", font=("Arial", 14), bg="black", fg="green").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.voter_id_entry = tk.Entry(input_frame, font=("Arial", 14), bg="black", fg="green", insertbackground="green")
        self.voter_id_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(input_frame, text="Select Candidate:", font=("Arial", 14), bg="black", fg="green").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.candidates = list(self.vote_counts.keys())
        self.candidate_var = tk.StringVar(value=self.candidates[0])
        tk.OptionMenu(input_frame, self.candidate_var, *self.candidates).grid(row=1, column=1, padx=10, pady=5)

        # Submit Button
        tk.Button(self.root, text="Submit Vote", font=("Arial", 14, "bold"), bg="green", fg="black", command=self.submit_vote).pack(pady=20)

        # Blockchain Display
        tk.Label(self.root, text="Blockchain Records:", font=("Arial", 14), bg="black", fg="green").pack(anchor="w", padx=20)
        self.blockchain_text = tk.Text(self.root, font=("Arial", 12), bg="black", fg="green", height=15, width=80, state=tk.DISABLED)
        self.blockchain_text.pack(padx=20, pady=10)

        self.update_blockchain_display()

    def submit_vote(self):
        voter_id = self.voter_id_entry.get()  # Get the entered voter ID
        candidate = self.candidate_var.get()  # Get the selected candidate

        if voter_id not in self.valid_voter_ids:
            messagebox.showerror("Invalid Voter ID", "This voter ID is not authorized.")
        elif voter_id in self.voter_ids_used:
            messagebox.showerror("Duplicate Vote", "This voter ID has already been used.")
        else:
            # Add the vote to the blockchain
            self.blockchain.add_vote(voter_id, candidate)
            self.voter_ids_used.add(voter_id)  # Mark the voter ID as used
            self.vote_counts[candidate] += 1  # Update the vote count
            self.update_blockchain_display()  # Refresh the blockchain display

            # Check if the candidate has won
            if self.vote_counts[candidate] >= 3:
                self.display_results(candidate)

            # Success message
            messagebox.showinfo("Vote Submitted", f"Your vote for {candidate} has been recorded!")
            self.voter_id_entry.delete(0, tk.END)  # Clear the voter ID field

    def update_blockchain_display(self):
        self.blockchain_text.config(state=tk.NORMAL)
        self.blockchain_text.delete(1.0, tk.END)  # Clear the display
        for block in self.blockchain.chain:
            # Display information about each block
            block_info = f"Block {block.index}:\nVoter ID: {block.voter_id}\nCandidate: {block.candidate}\nHash: {block.hash}\n\n"
            self.blockchain_text.insert(tk.END, block_info)
        self.blockchain_text.config(state=tk.DISABLED)

    def display_results(self, winner):
        # Display the winner in a new window
        results_window = tk.Toplevel(self.root)
        results_window.title("Election Results")
        results_window.geometry("400x200")
        results_window.config(bg="black")

        tk.Label(results_window, text=f"🎉 WINNER: {winner} 🎉", font=("Arial", 16, "bold"), bg="black", fg="green").pack(pady=20)
        tk.Label(results_window, text="Final Vote Counts:", font=("Arial", 14), bg="black", fg="green").pack()
        results_text = "\n".join([f"{candidate}: {count} votes" for candidate, count in self.vote_counts.items()])
        tk.Label(results_window, text=results_text, font=("Arial", 12), bg="black", fg="green").pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    blockchain = Blockchain()
    app = VotingApp(root, blockchain)
    root.mainloop()
