# Définir un port USB dans ubuntu #

Pour ce qui est propre au robot, copier le fichier “10-heron.rules” situé dans FixationPortsUSB dans le dossier de ubuntu “/lib/udev/rules.d/”, puis redémarrer le système 

### Les ports seront les suivants : ###

* IMU : “/dev/imu” 
* Driver Moteur Roboteq front : “/dev/roboteq_front” SEULEMENT BRANCHER SUR LE HUB USB PORT 10 
* Driver Moteur Roboteq back : “/dev/roboteq_back” SEULEMENT BRANCHER SUR LE HUB USB PORT 3 
* Driver Moteur glissière : “/dev/winch” 
* Capteur batterie : “/dev/battery” 
* Lidar : “/dev/lidar”  

ATTR sont les attributs des périphériques, ce qui va permettre de différencier les périphériques 

SYMLINK fait le lien entre le port sur lequel est branché le périphérique et le nom que l’on veut donner à ce port 

KERNELS est relié au port USB physique  

### Pour écrire une règle : ###

http://guidella.free.fr/General/ecrireReglePourUdev.html#sec10 
