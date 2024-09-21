import subprocess
import discord
import asyncio
from datetime import date
import calendar
import locale

def bool_find_lines_with_words(file_path, words):
    compare = False
    with open(file_path, 'r', encoding='utf-8') as file:
        #on parcourt le site
        for line in file:
            if compare:
                if all(word in line for word in words):
                    #S'il n'est pas marqué en reporté alors c'est bon
                    if "Reporté" not in line.strip():
                        return True
            #on vérifie si one piece est sorti aujourd'hui   
            if "<!-- "+quelJour()+" -->" in line:
                compare = True
            #si on a parcouru aujourd'hui sans trouver one piece alors on verra demain
            elif "<!-- "+quelJourDemain()+" -->" in line:
                return False
                          
    return False

def bool_find_sortieAnime(file_path, anime):
    compare = False
    compare2 = False
    with open(file_path, 'r', encoding='utf-8') as file:
        #on parcourt le site
        for line in file:
            if compare:
                if anime in line:
                    return True
            #si on arrive à cette étape alors on commence la comparaison
            if "Derniers scans ajoutés" in line:
                compare = True
            #si on arrive ici alors il n'y a pas eu de nouveau scan de OPM
            elif "Derniers contenus sortis" in line:
                print("pas le bon jour")
                return False

def goCurl():
    # Open the file in write mode
    file_path = "chemin/animeSamaIndex.html"
    file_handle = open(file_path, 'w')
    try:
        # Run the subprocess and redirect stdout to the file
        subprocess.check_call(['curl', "https://anime-sama.fr/"], stdout=file_handle)
        print("bien curl")
    finally:
        # Ensure the file is closed
        file_handle.close()
        print("bien fermé")

def quelJour():
    #jour = calendar.LocaleTextCalendar(firstweekday=0, locale='fr_FR.UTF-8')
    locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
    ma_date = date.today()
    # Obtenir le jour de la semaine (0 pour lundi, 6 pour dimanche)
    jour_semaine_index = ma_date.weekday()
    # Obtenir le nom du jour de la semaine en français
    nom_jour = calendar.day_name[jour_semaine_index]
    return nom_jour

def quelJourDemain():
    #jour = calendar.LocaleTextCalendar(firstweekday=0, locale='fr_FR.UTF-8')
    locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
    ma_date = date.today()
    # Obtenir le jour de la semaine (0 pour lundi, 6 pour dimanche)
    jour_semaine_index = ma_date.weekday()+1
    # Obtenir le nom du jour de la semaine en français
    #Dans le cas de dimanche+1 on renvoie lundi
    if jour_semaine_index == 7:
        return "Lundi"
    else:
        nom_jour = calendar.day_name[jour_semaine_index]
    return nom_jour

def main():
    #curl l'accueil
    goCurl()
    file_path = 'chemin/animeSamaIndex.html'
    wordsOnePiece = ['One Piece', 'Scan', 'VF']  # Remplacez par vos mots spécifiques
    client = discord.Client(intents=discord.Intents.default())
    client.messages = True
    client.message_content = True
    client.intents.members = True

    @client.event
    async def on_ready():
        print("Le bot est prêt !")
        canal = client.get_channel(123)
        if bool_find_lines_with_words(file_path, wordsOnePiece) :
            await canal.send("Nouveau chapitre de OnePiece !")
        if bool_find_sortieAnime(file_path, "One Punch Man") :
            await canal.send("Nouveau chapitre de One Punch Man !")
        await asyncio.sleep(8)  # Attend 8 secondes
        #on ferme le tout
        await client.close()
    #on run le tout
    client.run("***")

main()
