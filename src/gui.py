import tkinter as tk

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
    compose_button = tk.Button(window, text="Compose Music", command=lambda: print("Button clicked!"))
    compose_button.pack(pady=20)

    # Start the GUI event loop
    window.mainloop()

if __name__ == "__main__":
    main()