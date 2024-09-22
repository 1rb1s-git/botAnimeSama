import subprocess
import discord
import asyncio
from datetime import date
import calendar
import locale
import os
from dotenv import load_dotenv

def bool_find_lines_with_words():
    compare = False
    words = os.getenv('WORDS').split(",")
    with open(os.getcwd()+"/animeSamaIndex.html", 'r', encoding='utf-8') as file:
        #on parcourt le site, si on est dimanche c'est la fonction showhide() qui apparait en suivant
        if quelJour().lower()=="dimanche":
            for line in file:
                if compare:
                    if all(word in line for word in words ):
                        print("nouveau scan")
                        #S'il n'est pas marqué en reporté alors c'est bon
                        if "Reporté" not in line.strip():
                            return True
                #on vérifie si one piece est sorti aujourd'hui   
                if "<!-- "+quelJour()+" -->" in line:
                    compare = True
                #si on a parcouru aujourd'hui sans trouver one piece alors on verra demain
                elif "showhide()" in line:
                    print("pas de nouvelle sortie")
                    return False
        else:
            for line in file:
                if compare:
                    print(line)
                    if all(word in line for word in words ):
                        print("nouveau scan")
                        #S'il n'est pas marqué en reporté alors c'est bon
                        if "Reporté" not in line.strip():
                            return True
                #on vérifie si one piece est sorti aujourd'hui   
                if "<!-- "+quelJour()+" -->" in line:
                    print("on est "+quelJour())
                    compare = True
                #si on a parcouru aujourd'hui sans trouver one piece alors on verra demain
                elif "<!-- "+quelJourDemain()+" -->" in line:
                    return False       
    return False

def bool_find_sortieAnime():
    compare = False
    with open(os.getcwd()+"/animeSamaIndex.html", 'r', encoding='utf-8') as file:
        #on parcourt le site
        for line in file:
            if compare:
                if os.getenv("ANIME_ALEATOIRE") in line:
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
    file_handle = open(os.getcwd()+"/animeSamaIndex.html", 'w')
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
    load_dotenv()
    #curl l'accueil
    goCurl()
    client = discord.Client(intents=discord.Intents.default())
    client.messages = True
    client.message_content = True
    client.intents.members = True

    @client.event
    async def on_ready():
        print("Le bot est prêt !")
        canal = client.get_channel(int(os.getenv('CHANNEL')))
        if bool_find_lines_with_words() :
            await canal.send(os.getenv('MESSAGE_REGULIER'))
        if bool_find_sortieAnime() :
            await canal.send(os.getenv('MESSAGE_ALEATOIRE'))
        await asyncio.sleep(8)  # Attend 8 secondes
        #on ferme le tout
        await client.close()
    #on run le tout
    client.run(os.getenv('TOKEN'))

main()

