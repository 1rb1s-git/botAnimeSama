<div align="center">
    <img src="res/botManga.png" width="300px"/>
</div>
J'en avais marre d'aller sur le site ANIME SAMA pour vérifier si un nouveau scan était sorti. J'ai donc fait un script updateManga.py qui curl la page d'accueil de https://anime-sama.fr/ pour savoir si un nouveau scan/anime est disponible et qui envoie une notification discord si c'est le cas.

# 1 : Créer le bot discord

Il faut d'abord créer notre bot discord qui nous enverras les notifications, vous pouvez suivre cette documentation : https://www.docstring.fr/blog/creer-un-bot-discord-avec-python/#creation-du-bot
Le lien pour créer le bot directement : https://discord.com/developers/
Pensez bien à copier le token de création, vous en aurez besoin pour run le bot.
Dans notre cas nous n'aurons besoin que d'envoyer des messages en permissions : 
<div align="center">
    <img src="res/permissionsBot.png" width="600px"/>
</div>

# 2 : Personnaliser le script 

Le script contient deux fonctions pour deux types de sorties différentes. 

## 2.1 : Sortie régulière

Il y a les scans qui sortent toutes les semaines, et qui sont donc dans la partie "SORTIES DU ***" avec le jour d'aujourd'hui. Dans mon cas c'est one piece, on veut juste savoir s'il est reporté.
Cela correspond à la fonction bool_find_lines_with_words().
Les modifications que vous aurez à faire seront d'aller modifier les mots dans la variable WORDS du fichier .env. 
Dans le cas d'un anime voici à quoi pourrait correspondre les mots : 
```
WORDS = One piece,anime,vostfr
```
Il suffit d'aller voir le code source animeSamaIndex.html en cas de doute.
N'oubliez pas d'adapter votre message MESSAGE_REGULIER en fonction.
## 2.2 : Sortie aléatoire

A contrario, il y a des scans qui sortent de manière aléatoire. Dans mon cas One Punch Man, on va donc aller dans la partie "DERNIERS SCANS AJOUTÉS". Cette méthode est d'ailleurs à privilégier pour plus de fiabilité, elle correspond à la fonction bool_find_sortieAnime(). 
Il faut modifier le nom de l'anime dans ANIME_ALEATOIRE ainsi que MESSAGE_ALEATOIRE dans le fichier .env.

## 2.3 : Ajouter les infos discord

Il faut maintenant modifier votre numéro de channel où seront envoyés les notifications dans CHANNEL. Le numéro peut être obtenu en faisant un clique droit sur le channel puis "Copy Link".
Il faut ensuite mettre le token du bot dans TOKEN.
Il peut être regénéré dans Bot > TOKEN > Reset Token si vous l'avez oubliez depuis de le portail développeur.

# 3 : Lancer le script

Il est maintenant temps de tester le script. Téléchargez le avec les requirements et lancez la commande : 
```
pip install -r requirements.txt
```
Maintenant 
```
python3 update.py
```
Vous devriez avoir reçu la notification si le scan est sorti, je vous invite à le tester sur les nouveaux scans du jour si ce n'est pas le cas. 

# 4 : Lancement automatique

Tout l'intérêt du script est qu'il soit lancé de manière automatique. Vous pouvez l'ajouter à une tâche cron sur votre PC ou directement sur votre serveur NAS : https://www.maxy.fr/article/programmer-une-tache-cron-depuis-un-nas-synology
Voici la commande que vous pouvez ajouter :
```
/bin/bash -c 'source chemin/.venvAnime/bin/activate && python chemin/updateManga.py'
```
