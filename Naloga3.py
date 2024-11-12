import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import matplotlib.pyplot as plt
import numpy as np


class KepnerTregoeMetodaApp:
    def __init__(self, master):
        self.master = master
        master.title("Kepner-Tregoe Metoda")

        # Parameters
        self.parametri = []
        self.utezi = []
        self.alternative = {}

        self.widgets()

    def widgets(self):
        # parametre
        self.param_label = tk.Label(self.master, text="Vnesi parametre (vejica med njimi!):")
        self.param_label.pack()

        self.param_entry = tk.Entry(self.master, width=50)
        self.param_entry.pack()

        self.dodaj_param_button = tk.Button(self.master, text="Dodaj parametre", command=self.dodaj_parametre)
        self.dodaj_param_button.pack()

        # utezi
        self.utezi_label = tk.Label(self.master, text="Doloci utezi (0-10) za vsak parametar:")
        self.utezi_label.pack()

        self.doloci_weight_button = tk.Button(self.master, text="Dodaj utezi", command=self.doloci_utezi)
        self.doloci_weight_button.pack()

        # alternative
        self.alternative_label = tk.Label(self.master, text="Vnesi alternative (vejica med njimi!):")
        self.alternative_label.pack()

        self.alternative_entry = tk.Entry(self.master, width=50)
        self.alternative_entry.pack()

        self.dodaj_alternative_button = tk.Button(self.master, text="Dodaj alternative", command=self.dodaj_alternative)
        self.dodaj_alternative_button.pack()

        # vrednosti alternativ
        self.vrednosti_label = tk.Label(self.master, text="Dodaj vrednosti (0-10) za vsaka alternativa:")
        self.vrednosti_label.pack()

        self.doloci_vrednosti_button = tk.Button(self.master, text="Doloci vrednosti", command=self.doloci_vrednosti)
        self.doloci_vrednosti_button.pack()

        # risanje graf
        self.calculate_button = tk.Button(self.master, text="Izracunaj in izrisi grafov", command=self.calculate_and_plot)
        self.calculate_button.pack()

        # analiza senzitivnosti
        self.sensitivity_label = tk.Label(self.master, text="Izberi parametar za analizo senzitivnosti:")
        self.sensitivity_label.pack()

        self.sensitivity_button = tk.Button(self.master, text="Zazeni analizo senzitivnosti", command=self.sensitivity_analysis)
        self.sensitivity_button.pack()

    def dodaj_parametre(self):
        params = self.param_entry.get().split(",")
        self.parametre = [param.strip() for param in params]
        messagebox.showinfo("Info", "Parametre so dodane!")

    def doloci_utezi(self):
        self.utezi = []
        for param in self.parametre:
            utez = simpledialog.askinteger("Input", f"Doloci utez za  {param} (0-10):", minvalue=0, maxvalue=10)
            self.utezi.append(utez)

    def dodaj_alternative(self):
        alternatives = self.alternative_entry.get().split(",")
        self.alternatives = {alt.strip(): [] for alt in alternatives}
        messagebox.showinfo("Info", "Alternative so dodane!")

    def doloci_vrednosti(self):
        for alt in self.alternatives.keys():
            vrednosti = simpledialog.askstring("Input", f"Doloci vrednost za {alt} (vejica med njimi):")
            seznam_vrednosti = [int(vrednost) for vrednost in vrednosti.split(",") if vrednost.isdigit()]
            if len(seznam_vrednosti) == len(self.parametre):
                self.alternative[alt] = seznam_vrednosti
            else:
                messagebox.showerror("Error", "Stevilo vrednosti naj se ujema z stevilo parametrov!")

    def calculate_and_plot(self):
        if not self.alternative or not self.utezi:
            messagebox.showerror("Error", "Dodaj alternative in utezi prvic!")
            return

        rezultat = {alt: sum(np.array(vrednosti) * np.array(self.utezi)) for alt, vrednosti in self.alternative.items()}
        self.izris_grafov(rezultat)

    def izris_grafov(self, rezultat):
        plt.figure(figsize=(12, 6))

        # vrednosti alternativ
        plt.subplot(1, 2, 1)
        plt.bar(rezultat.keys(), rezultat.values())
        plt.title("Primerjava vrednosti alternativ")
        plt.xlabel("Alternative")
        plt.ylabel("Vrednosti")

        # utezi parametrov
        plt.subplot(1, 2, 2)
        plt.bar(self.parametre, self.utezi)
        plt.title("Primerjava utezi parametrov")
        plt.xlabel("Parametre")
        plt.ylabel("Utezi")

        plt.tight_layout()
        plt.show()

    def sensitivity_analysis(self):
        param_index = simpledialog.askinteger("Input", "Izberi index od tega parametra za analiza senzitivnosti:", minvalue=1, maxvalue=len(self.parametre))
        param_index -= 1

        if param_index < 0 or param_index >= len(self.utezi):
            messagebox.showerror("Error", "Nevaliden index parametra!")
            return

        utez_original = self.utezi[param_index]
        sensitivity_scores = {alt: [] for alt in self.alternatives}

        for utez in range(11):
            self.utezi[param_index] = utez
            for alt, values in self.alternative.items():
                score = sum(np.array(values) * np.array(self.utezi))
                sensitivity_scores[alt].append(score)

        self.utezi[param_index] = utez_original

        # Plot sensitivity analysis
        plt.figure(figsize=(8, 6))
        for alt, scores in sensitivity_scores.items():
            plt.plot(range(11), scores, label=alt)

        plt.title(f"Analiza senzitivnosti za parametar: {self.parametre[param_index]}")
        plt.xlabel("Utezi parameter (0-10)")
        plt.ylabel("Vrednosti alternative")
        plt.legend()
        plt.grid(True)
        plt.show()


if __name__ == "__main__":
    root = tk.Tk()
    app = KepnerTregoeMetodaApp(root)
    root.mainloop()
