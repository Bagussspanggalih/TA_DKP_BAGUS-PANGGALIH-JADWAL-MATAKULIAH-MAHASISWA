import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import re

class ProgramJadwalMatakuliah:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("JADWAL.KU")
        self.window.geometry("800x460")

        self.jadwal_list = []

        self.background_image = Image.open("dkp1.jpg")
        self.background_image = self.background_image.resize((800, 460))  # Sesuaikan dengan resolusi jendela
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.background_label = tk.Label(self.window, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.frame = tk.Frame(self.window, bg="")
        self.frame.pack(pady=10, anchor=tk.W)

        self.label_matakuliah = tk.Label(self.frame, text="Matakuliah:")
        self.label_matakuliah.grid(row=0, column=0, sticky=tk.W)

        self.entry_matakuliah = tk.Entry(self.frame)
        self.entry_matakuliah.grid(row=0, column=1)

        self.label_jam_masuk = tk.Label(self.frame, text="Jam Masuk:")
        self.label_jam_masuk.grid(row=1, column=0, sticky=tk.W)

        self.entry_jam_masuk_jam = tk.Entry(self.frame, validate="key", width=5)
        self.entry_jam_masuk_jam.configure(validatecommand=(self.entry_jam_masuk_jam.register(self.validate_jam_input), "%P"))
        self.entry_jam_masuk_jam.grid(row=1, column=1)

        self.label_separator1 = tk.Label(self.frame, text=":", padx=5)
        self.label_separator1.grid(row=1, column=2)

        self.entry_jam_masuk_menit = tk.Entry(self.frame, validate="key", width=5)
        self.entry_jam_masuk_menit.configure(validatecommand=(self.entry_jam_masuk_menit.register(self.validate_jam_input), "%P"))
        self.entry_jam_masuk_menit.grid(row=1, column=3)

        self.label_jam_selesai = tk.Label(self.frame, text="Jam Selesai:")
        self.label_jam_selesai.grid(row=2, column=0, sticky=tk.W)

        self.entry_jam_selesai_jam = tk.Entry(self.frame, validate="key", width=5)
        self.entry_jam_selesai_jam.configure(validatecommand=(self.entry_jam_selesai_jam.register(self.validate_jam_input), "%P"))
        self.entry_jam_selesai_jam.grid(row=2, column=1)

        self.label_separator2 = tk.Label(self.frame, text=":", padx=5)
        self.label_separator2.grid(row=2, column=2)

        self.entry_jam_selesai_menit = tk.Entry(self.frame, validate="key", width=5)
        self.entry_jam_selesai_menit.configure(validatecommand=(self.entry_jam_selesai_menit.register(self.validate_jam_input), "%P"))
        self.entry_jam_selesai_menit.grid(row=2, column=3)

        self.frame_hari = tk.Frame(self.window, bg="")
        self.frame_hari.pack(anchor=tk.W)

        self.label_hari = tk.Label(self.frame_hari, text="Hari:")
        self.label_hari.pack(side=tk.LEFT)

        self.combo_hari = ttk.Combobox(self.frame_hari, values=["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"], state="readonly")
        self.combo_hari.pack(side=tk.LEFT)

        self.button_tambah = tk.Button(self.window, text="Tambah Jadwal", command=self.tambah_jadwal)
        self.button_tambah.pack()

        self.button_hapus = tk.Button(self.window, text="Hapus Jadwal", command=self.hapus_jadwal)
        self.button_hapus.pack()

        self.jadwal_listbox = ttk.Treeview(
            self.window, columns=("Hari", "Matakuliah", "Jam Masuk", "Jam Selesai"), show="headings", 
            style="Custom.Treeview"
        )
        self.jadwal_listbox.heading("Hari", text="Hari")
        self.jadwal_listbox.heading("Matakuliah", text="Matakuliah")
        self.jadwal_listbox.heading("Jam Masuk", text="Jam Masuk")
        self.jadwal_listbox.heading("Jam Selesai", text="Jam Selesai")
        self.jadwal_listbox.pack(pady=10)

        self.button_keluar = tk.Button(self.window, text="Keluar", command=self.keluar)
        self.button_keluar.pack()

        self.should_exit = False

    def tambah_jadwal(self):
        matakuliah = self.entry_matakuliah.get()
        jam_masuk_jam = self.entry_jam_masuk_jam.get()
        jam_masuk_menit = self.entry_jam_masuk_menit.get()
        jam_selesai_jam = self.entry_jam_selesai_jam.get()
        jam_selesai_menit = self.entry_jam_selesai_menit.get()
        hari = self.combo_hari.get()
        jadwal = (hari, matakuliah, f"{jam_masuk_jam}:{jam_masuk_menit}", f"{jam_selesai_jam}:{jam_selesai_menit}")

        if self.is_jadwal_conflict(jadwal):
            messagebox.showerror("Konflik Jadwal", "Jadwal matakuliah bertabrakan dengan jadwal yang ada!")
        else:
            self.jadwal_list.append(jadwal)
            self.jadwal_listbox.insert("", tk.END, values=jadwal)
            messagebox.showinfo("Sukses", "Jadwal matakuliah berhasil ditambahkan.")

    def hapus_jadwal(self):
        selected_items = self.jadwal_listbox.selection()
        if selected_items:
            for item in selected_items:
                index = self.jadwal_listbox.index(item)
                jadwal = self.jadwal_list[index]
                self.jadwal_list.remove(jadwal)
                self.jadwal_listbox.delete(item)
            messagebox.showinfo("Sukses", "Jadwal matakuliah berhasil dihapus.")
        else:
            messagebox.showinfo("Perhatian", "Tidak ada jadwal matakuliah yang dipilih.")

    def is_jadwal_conflict(self, new_jadwal):
        for jadwal in self.jadwal_list:
            hari, matakuliah, jam_masuk, jam_selesai = jadwal
            if hari == new_jadwal[0]:
                if (jam_masuk <= new_jadwal[3] and jam_selesai > new_jadwal[2]) or (
                    new_jadwal[2] <= jam_selesai and new_jadwal[3] > jam_masuk
                ):
                    return True
        return False

    def keluar(self):
        self.should_exit = True
        self.window.destroy()

    def validate_jam_input(self, value):
        pattern = r'^\d{1,2}$'
        if re.match(pattern, value):
            return True
        elif value == "":
            return True
        else:
            return False

    def run(self):
        self.background_label.image = self.background_photo  # Keep a reference to the image to prevent garbage collection
        
        while not self.should_exit:
            try:
                self.window.update()
            except tk.TclError:
                break

program = ProgramJadwalMatakuliah()
program.run()
