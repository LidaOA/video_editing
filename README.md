# video_editing

Ce projet permet d'effectuer un montage vidéo simplifié et automatisé sous Python.

Pour l

Le projet nécessite obligatoirement (pour l'instant) :

+ un dossier nommé "output" dans le repértoire courant contenant les vidéos que l'utilisateur souhaite monter

soit (au choix) : 

+ deux dossiers dans le répertoire courant nommés "input_data" et "input_backsound"
+ deux paramètres en arguments, nommés "folder_videos" et "folder_audios"

Pour lancer le programme, il suffit d'exécuter cette ligne de commande :

```
python main.py
```

Par défaut, le programme va chercher les informations dans les dossiers "input_data" et "input_backsound" 

Autrement on lance en ajoutant les 2 arguments explicités un peu plus avec :
```
python main.py --folder_videos __chemin vers le dossier vidéos__  --folder_audios __chemin vers le dossier des fonds sonores__
```

Le montage se compose d'éléments modifiables au niveau du code par les éléments suivants :

+ Un fondu sur la vidéo à monter au niveau de l'audio de 2 sec en entrée et de 5 secondes en sortie, aisi qu'un fondu au noir sur l'image d'une seconde au début de la vidéo et d'une seconde à la fin de la vidéo
+ Un fondu au niveau du fond sonore de 2 sec en entrée et de 5 secondes en sortie

Le projet permet aussi de récupérer des captures d'écran utilisables (entre autres) pour des miniatures.
Le nombre de miniatures effectué est compris entre 1 et 6 (inclus) et reste lui aussi modifiable à l'intérieur du code. 
