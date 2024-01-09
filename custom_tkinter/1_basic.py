import customtkinter as ctk

ctk.set_appearance_mode("Dark")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

window = ctk.CTk()  # create CTk window like you do with the Tk window
window.geometry("400x240")

label = ctk.CTkLabel(window, text='A ctk Label', fg_color = 'red', text_color='white')
label.pack()

window.mainloop()