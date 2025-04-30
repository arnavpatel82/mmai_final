import tkinter as tk
from emo2music import *

def main():
    # Create the main window
    window = tk.Tk()
    window.title("Emotion to Music Generator")
    window.geometry("400x300")

    # Label
    label = tk.Label(window, text="Enter your phrase:")
    label.pack(pady=10)

    # Text entry
    text_entry = tk.Entry(window, width=40)
    text_entry.pack(pady=10)

    # Button
    def compose_music():
        user_text = text_entry.get()
        if user_text.strip():
            text_to_music(user_text, output_file="media/output.mid")
            print("Music generated and saved to media/output.mid!")

    compose_button = tk.Button(window, text="Compose Music", command=compose_music)
    compose_button.pack(pady=20)

    # Start the GUI event loop
    window.mainloop()

if __name__ == "__main__":
    main()