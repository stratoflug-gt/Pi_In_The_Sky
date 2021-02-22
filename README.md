# Pi_In_The_Sky
Files associated with the flying pi.

# pits-master: 
A copy of the Pi-in-the-sky pits-software modified for our use.

# Heizungssteuerung.py:
Software which controls the heating-circuit, featuring different variables adjustable in the code.

------------------------------------------------------------------------------------------------------------------

To download the software use the following command (verify the current working directrory is the root directory):
  > wget https://raw.githubusercontent.com/stratoflug-gt/Pi_In_The_Sky/main/Heizungssteuerung.py

------------------------------------------------------------------------------------------------------------------

To test the software complete the following procedure:

Open Heizungssteuerung.py by typing:
  > sudo nano Heizungssteuerung.py
  
Then change the variable <testMode> to <True>. Save and exit the document.

To start the script type:
  > python3 Heizungssteurung.py

You should now see output including four different temperature values.

------------------------------------------------------------------------------------------------------------------

In order to enable auto start open the file rc.local by typing:
  > sudo nano /etc/rc.local

Then add the following line to the file:
  > sudo python3 Heizungssteuerung.py & 

Then save and close the file. The program should now start automatically.
