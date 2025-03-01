from deep_translator import GoogleTranslator, single_detection
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image
import pytesseract
from gtts import gTTS
import os
import ttkbootstrap as tb  # 🎨 Thème moderne pour Tkinter
from PIL import Image, ImageTk
import pyperclip  # Pour copier dans le presse-papiers
from tkinter import filedialog
import speech_recognition as sr# pour 
from tkinter import Tk, Text, Button
from PIL import Image, ImageTk
from tkinter import PhotoImage  # Utiliser ce module pour charger les images



# Configuration de Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  

# Dictionnaire des langues
langues = {
    "Français": "fr",
    "Anglais": "en",
    "Espagnol": "es",
    "Allemand": "de",
    "Russe": "ru",
    "Chinois": "zh-CN",
    "Arabe": "ar",
    "Japonais": "ja",
    "Hindi": "hi",
    "Bengali": "bn",
    "Portugais": "pt",
    "Lahnda (Punjabi)": "lzh",
    "Javanais": "jv",
    "Coréen": "ko",
    "Telugu": "te",
    "Marathi": "mr",
    "Turck": "tr",
    "Vietnamien": "vi",
    "Italien": "it",
    "Thaïlandais": "th",
    "Gujarati": "gu",
    "Kannada": "kn",
    "Persan": "fa",
    "Polonais": "pl",
    "Pashto": "ps",
    "Malayalam": "ml",
    "Ouzbek": "uz",
    "Sundanais": "su",
    "Hausa": "ha",
    "Amharique": "am",
    "Yoruba": "yo",
    "Birmane": "my",
    "Maïthili": "mai",
    "Mongol": "mn",
    "Tchèque": "cs",
    "Sinhala": "si",
    "Tagalog": "tl",
    "Arroz": "ar",
    "Polonais": "pl",
    "Néerlandais": "nl",
    "Suédois": "sv",
    "Hébreu": "he",
    "Danois": "da",
    "Finnois": "fi",
    "Norvégien": "no",
    "Grec": "el",
    "Hongrois": "hu",
    "Tchétchène": "ce",
    "Cantonais": "zh-HK",
    "Géorgien": "ka",
    "Indonésien": "id",
    "Serbe": "sr",
    "Croate": "hr",
    "Lituanien": "lt",
    "Letton": "lv",
    "Slovaque": "sk",
    "Slovène": "sl",
    "Bosnien": "bs",
    "Filipino": "tl",
    "Macedonien": "mk",
    "Albanais": "sq",
    "Basque": "eu",
    "Catalan": "ca",
    "Galicien": "gl",
    "Basque": "eu",
    "Breton": "br",
    "Wolof": "wo",
    "Nepali": "ne",
    "Bengali": "bn",
    "Sotho": "st",
    "Kinyarwanda": "rw",
    "Tigrinya": "ti",
    "Haitien créole": "ht",
    "Chichewa": "ny",
    "Kazakh": "kk",
    "Tamil": "ta",
    "Somali": "so",
    "Khmer": "km",
    "Lao": "lo",
    "Bengali": "bn",
    "Igbo": "ig",
    "Xhosa": "xh",
    "Sesotho": "st",
    "Malais": "ms",
    "Malaise": "ml",
    "Tagalog": "tl",
    "Fijian": "fj",
    "Zoulou": "zu",
    "Maori": "mi",
    "Twi": "tw",
    "Sinhalese": "si",
    "Kazak": "kk",
    
}


# Historique des traductions
historique_traductions = []


# 🌟 Fonction pour extraire du texte d'une image
def extraire_texte_image():
    fichier_image = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")])
    if fichier_image:
        try:
            image = Image.open(fichier_image)
            texte_extrait = pytesseract.image_to_string(image)
            entree_texte.delete("1.0", tk.END)
            entree_texte.insert(tk.END, texte_extrait)
        except Exception as e:
            entree_texte.delete("1.0", tk.END)
            entree_texte.insert(tk.END, f"Erreur d'extraction : {e}")

# 🌟 Fonction de traduction
def traduire():
    texte = entree_texte.get("1.0", tk.END).strip()
    
    if not texte:
        sortie_texte.config(state=tk.NORMAL)
        sortie_texte.delete("1.0", tk.END)
        sortie_texte.insert(tk.END, "Veuillez entrer un texte à traduire.")
        sortie_texte.config(state=tk.DISABLED)
        return

    langue_source_nom = langue_source_var.get().strip()

    # 🔍 Détection automatique de la langue
    if langue_source_nom == "Auto-détection":
        try:
            langue_source = single_detection(texte, api_key="YOUR_API_KEY")  # Remplace par une clé API si nécessaire
        except Exception as e:
            sortie_texte.config(state=tk.NORMAL)
            sortie_texte.delete("1.0", tk.END)
            sortie_texte.insert(tk.END, f"Erreur de détection : {e}")
            sortie_texte.config(state=tk.DISABLED)
            return
    else:
        langue_source = langues.get(langue_source_nom, "en")

    langue_cible_nom = langue_cible_var.get().strip()
    langue_cible = langues.get(langue_cible_nom, "fr")

    try:
        translator = GoogleTranslator(source=langue_source, target=langue_cible)
        traduction = translator.translate(texte)
        
        sortie_texte.config(state=tk.NORMAL)
        sortie_texte.delete("1.0", tk.END)
        sortie_texte.insert(tk.END, f"[Langue détectée : {langue_source}]\n{traduction}")
        sortie_texte.config(state=tk.DISABLED)

        # Ajouter l'entrée au historique
        historique_traductions.append(f"[{langue_source}] → [{langue_cible}] : {traduction}")

    except Exception as e:
        sortie_texte.config(state=tk.NORMAL)
        sortie_texte.delete("1.0", tk.END)
        sortie_texte.insert(tk.END, f"Erreur de traduction : {e}")
        sortie_texte.config(state=tk.DISABLED)

# 🔊 Fonction pour lire la traduction
def lire_traduction():
    texte = sortie_texte.get("1.0", tk.END).strip()
    if texte:
        langue_cible = langues.get(langue_cible_var.get().strip(), "fr")
        tts = gTTS(text=texte, lang=langue_cible)
        tts.save("traduction.mp3")
        os.system("start traduction.mp3")  # Ouvre le fichier audio

# 📋 Copier la traduction dans le presse-papiers
def copier_traduction():
    texte = sortie_texte.get("1.0", tk.END).strip()
    if texte:
        pyperclip.copy(texte)
        messagebox.showinfo("Copie réussie", "La traduction a été copiée dans le presse-papiers.")

# 📂 Sauvegarder la traduction dans un fichier texte
def sauvegarder_traduction():
   
    texte = sortie_texte.get("1.0", tk.END).strip()
    if texte:
        # Ouvre une boîte de dialogue pour choisir où enregistrer le fichier
        fichier = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Fichiers texte", "*.txt")])
        
        if fichier:  # Si un fichier a été sélectionné
            try:
                with open(fichier, "w", encoding="utf-8") as file:
                    file.write(texte)
                messagebox.showinfo("Enregistrement réussi", f"La traduction a été enregistrée dans {fichier}.")
            except Exception as e:
                messagebox.showerror("Erreur", f"Une erreur est survenue lors de l'enregistrement : {e}")
        else:
            messagebox.showwarning("Annulé", "L'enregistrement a été annulé.")
def filtrer_langues(event, combobox, variable):
    texte = variable.get().lower()
    langues_filtrees = [lang for lang in langues_tries if texte in lang.lower()]
    
    if langues_filtrees:  
        combobox["values"] = langues_filtrees
    else:
        combobox["values"] = langues_tries  # Réinitialise si aucune correspondance


def reconnaissance_vocale():
    messagebox.showinfo("Micro activé", "Vous pouvez parler maintenant...")



def ouvrir_google_traduction():
    phrase_traduite = zone_sortie.get("1.0", tk.END).strip()
    if phrase_traduite:
        url = f"https://translate.google.com/?sl=auto&tl=fr&text={phrase_traduite}&op=translate"
        webbrowser.open(url)
    else:
        messagebox.showwarning("Aucune traduction", "Veuillez d'abord traduire une phrase.")



# 🌟 Interface graphique (Tkinter avec ttkbootstrap)
root = tb.Window(themename="superhero")  # 🎨 Thème moderne
root.title("Rebec Traduction")
root.title("Rebec Traduction")
root.geometry("700x500")
root.minsize(500, 350)
root.resizable(True, True)  # Permet le redimensionnement


# Chargement de l'image
image = Image.open("C:\\Users\\hp\\Desktop\\pythonbasecertif\\traducteur\\rebec.png")
photo = ImageTk.PhotoImage(image)  

# Définition de l'icône de la fenêtre
root.iconphoto(False, photo)


frame = ttk.Frame(root, padding="10")
frame.pack(fill=tk.BOTH, expand=True)



ttk.Label(frame, text=" Texte à traduire :", font=("Arial", 15, "bold")).pack(anchor=tk.W)

# Zone de texte d'entrée avec un curseur
frame_texte_entree = ttk.Frame(frame)
frame_texte_entree.pack(fill=tk.BOTH, expand=True)

entree_texte = tk.Text(frame_texte_entree, height=8, width=60, font=("Arial", 12))
entree_texte.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)
entree_texte.configure(bg="white", fg="black")

scrollbar = ttk.Scrollbar(frame_texte_entree, orient="vertical", command=entree_texte.yview)
scrollbar.pack(side=tk.RIGHT, fill="y")
entree_texte.config(yscrollcommand=scrollbar.set)

# 🎙️ Fonction pour la reconnaissance vocale
def reconnaissance_vocale():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        sortie_texte.config(state=tk.NORMAL)
        sortie_texte.delete("1.0", tk.END)
        sortie_texte.insert(tk.END, "Écoute...")
        sortie_texte.config(state=tk.DISABLED)
        try:
            audio = recognizer.listen(source)
            texte_reconnu = recognizer.recognize_google(audio, language="fr-FR")
            entree_texte.delete("1.0", tk.END)
            entree_texte.insert(tk.END, texte_reconnu)
        except sr.UnknownValueError:
            messagebox.showerror("Erreur", "Je n'ai pas compris.")
        except sr.RequestError:
            messagebox.showerror("Erreur", "Problème de connexion.")

# 🎙️ Ajout d'un bouton Micro dans le premier carreau

bouton_micro = tb.Button(frame_texte_entree, text="🎤", command=reconnaissance_vocale, bootstyle="primary-outline")
bouton_micro.pack(side=tk.BOTTOM, pady=5)

lang_frame = ttk.Frame(frame)
lang_frame.pack(pady=5)


ttk.Label(lang_frame, text=" Langue source :", font=("Arial", 10)).grid(row=0, column=0, padx=5)
langue_source_var = tk.StringVar(value='Auto-détection')
langue_source_menu = ttk.Combobox(lang_frame, textvariable=langue_source_var, values=["Auto-détection"] + list(langues.keys()), state="readonly")
langue_source_menu.grid(row=0, column=1, padx=5)


ttk.Label(lang_frame, text="Langue cible :", font=("Arial", 10)).grid(row=0, column=2, padx=5)
langue_cible_var = tk.StringVar(value='Français')
langue_cible_menu = ttk.Combobox(lang_frame, textvariable=langue_cible_var, values= [
        "Mandarin", "Cantonais", "Wu", "Min", "Hakka", "Japonais", "Coréen",
        "Vietnamien", "Thaï", "Khmer", "Lao", "Birman", "Hindi", "Bengali",
        "Ourdou", "Tamoul", "Telugu", "Marathi", "Gujarati", "Punjabi",
        "Pashto", "Farsi", "Turc", "Kazakh", "Ouzbek", "Tadjik", "Mongol",
        "Malais", "Indonésien", "Tagalog",
        "Espagnol", "Portugais", "Anglais", "Français", "Créole haïtien",
        "Guarani", "Quechua", "Aymara", "Navajo", "Mapudungun", "Nahuatl",
        "Maya Yucatèque",
        "Russe", "Ukrainien", "Bélarusse", "Polonais", "Tchèque", "Slovaque",
        "Serbe", "Croate", "Bosnien", "Slovène", "Macédonien", "Bulgare",
        "Arabe", "Swahili", "Haoussa", "Amharique", "Oromo", "Somali",
        "Yoruba", "Igbo", "Fula", "Wolof", "Lingala", "Shona", "Xhosa",
        "Zulu", "Tswana",
        "Baoulé", "Bété", "Dioula", "Sénoufo", "Akan", "Krou", "Gouro",
        "Malinké",
        "Fon", "Yoruba", "Goun", "Bariba", "Dendi", "Adja", "Nagot",
        "Français", "Anglais", "Allemand", "Espagnol", "Italien", "Portugais",
        "Néerlandais", "Danois", "Suédois", "Norvégien", "Finnois", "Grec",
        "Hongrois", "Roumain", "Tchèque", "Polonais", "Slovaque", "Albanais",
        "Basque", "Maltese"])
langue_cible_menu.grid(row=0, column=3, padx=5)

# Trier les langues par ordre alphabétique
langues_tries = sorted(langues.keys())

# Mise à jour du menu déroulant pour la langue source
langue_source_menu["values"] = ["Auto-détection"] + langues_tries

# Mise à jour du menu déroulant pour la langue cible
langue_cible_menu["values"] = langues_tries

langue_source_menu.bind("<KeyRelease>", lambda event: filtrer_langues(event, langue_source_menu, langue_source_var))
langue_cible_menu.bind("<KeyRelease>", lambda event: filtrer_langues(event, langue_cible_menu, langue_cible_var))

btn_frame = ttk.Frame(frame)
btn_frame.pack(pady=10)

# 🎨 Boutons modernisés avec ttkbootstrap
bouton_traduire = tb.Button(btn_frame, text="🗣️ Traduire", command=traduire, bootstyle="primary-outline")
bouton_traduire.grid(row=1, column=0, padx=10)

bouton_image = tb.Button(btn_frame, text="📷 Extraire texte d'une image", command=extraire_texte_image, bootstyle="second-outline")
bouton_image.grid(row=1, column=1, padx=10)

bouton_audio = tb.Button(btn_frame, text="🔊 Écouter", command=lire_traduction, bootstyle="info-outline")
bouton_audio.grid(row=1, column=2, padx=10)

bouton_copier = tb.Button(btn_frame, text="📋 Copier", command=copier_traduction, bootstyle="warning-outline")
bouton_copier.grid(row=1, column=3, padx=10)

bouton_sauvegarder = tb.Button(btn_frame, text="💾 Sauvegarder", command=sauvegarder_traduction, bootstyle="success-outline")
bouton_sauvegarder.grid(row=1, column=4, padx=10)

ttk.Label(frame, text=" Traduction :", font=("Arial", 15, "bold")).pack(anchor=tk.W)

frame_texte_sortie = ttk.Frame(frame)
frame_texte_sortie.pack(fill=tk.BOTH, expand=True)

sortie_texte = tk.Text(frame_texte_sortie, height=8, width=60, font=("Arial", 12), state=tk.DISABLED)
sortie_texte.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)
sortie_texte.configure(bg="#D3D3D3", fg="black")

 # 🔊 Mise à jour de la fonction pour lire la traduction
def lire_traduction():
    texte = sortie_texte.get("1.0", tk.END).strip()
    if texte:
        langue_cible = langues.get(langue_cible_var.get().strip(), "fr")
        tts = gTTS(text=texte, lang=langue_cible)
        tts.save("traduction.mp3")
        os.system("start traduction.mp3")  # Ouvre le fichier audio

# 🎙️ Ajout d'un bouton Lecture dans le deuxième carreau
bouton_lecture = tb.Button(frame_texte_sortie, text="🔊", command=lire_traduction, bootstyle="primary-outline")
bouton_lecture.pack(side=tk.BOTTOM, pady=5)

scrollbar_sortie = ttk.Scrollbar(frame_texte_sortie, orient="vertical", command=sortie_texte.yview)
scrollbar_sortie.pack(side=tk.RIGHT, fill="y")
sortie_texte.config(yscrollcommand=scrollbar_sortie.set)

# 🌍 Bouton "Google Traduction"
bouton_google = tb.Button(frame_texte_sortie, text="🌍 Google", command=ouvrir_google_traduction, 
                          bootstyle="primary-outline")
bouton_google.pack(side=tk.BOTTOM, pady=5)
root.mainloop()