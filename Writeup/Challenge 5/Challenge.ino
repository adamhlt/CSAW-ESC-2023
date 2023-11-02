// Author : BitsFromBZH : Axel Gouriou, Adam Hesnault, Florian Lecoq
// Challenge number 5 : Sock and Roll
//
// This program needs to be uploaded in an additional Arduino which must be connected to the CSAW Arduino,
// Please follow the recommanded wiring explained in our report.
// It was made to automatically defeat the challenge.

// Variables globales :
int state = 0; // etat actuel de la machine à états
bool buzzerState = 1; // état dans lequel devrait être simulé le buzzer (ON ou OFF)
bool newBuzzerState = 1; // variable utilisée pour détecter les changements d'état sur la variable buzzerState
bool newState = 0;

// Fréquences émises vers la broche de mesure de fréquence de l'arduino du CSAW (A0).
unsigned long lowFreq = 1100; // Fréquence du buzzer lorsqu'il est ON
unsigned long highFreq = 31330; // Fréquence du buzzer lorsqu'il est OFF (High frequency)
unsigned long SOSFreq = 8364; // 8364 Hz SOS frequency !

// PINOUT of the arduino that hacks the CSAW's Arduino (only 3 pins need to be wired)
int emulatedMicrophoneDigitalOutput = 3; // broche 3 de l'arduino de hack, à relier à la broche 13 de l'arduino du CSAW
int pinGenFreq = 5; // Broche 5 de l'arduino de hack, à relier à la broche A0 de l'arduino du CSAW
// broche A0 Arduino de hack est à relier à la broche 10 de l'arduino du CSAW

void setup() {
  // Reglage de l'émulation des broches du microphone et de mesure de fréquence qui aurait du aller au buzzer
  pinMode(A0, INPUT); // broche de mesure de fréquence : INPUT
  pinMode(emulatedMicrophoneDigitalOutput,OUTPUT);
  digitalWrite(emulatedMicrophoneDigitalOutput,1); // default value = 1
  pinMode(pinGenFreq,OUTPUT); // broche de sortie de fréquence 1 KHz ou 31 KHz
  tone(pinGenFreq,1000); // default tone
  delay(1000); // délais de synchro at startup pour que l'arduino de hack démarre 1 sec après celle du CSAW
}

void loop() {

  // --- ROUTINE PERMANENTE frequencemetre ----------------------------
  // (elle tourne en continue)
  unsigned long duree_etat_haut1 = pulseIn(A0, HIGH);// mesure temps à l'état haut
  unsigned long duree_etat_bas1 = pulseIn(A0, LOW);  // mesure temps à l'état bas
  long periode = (duree_etat_haut1+duree_etat_bas1); // Calcul de la periode du signal mesuré
  long frequence = (1/ (periode*0.000001));          // Calcul de la fréquence du signal mesuré

  // On regarde si la fréquence est considérée comme haute ou basse en fonction d'un seuil.
  if((frequence < 2000) && (frequence > 500) )
  {
    // Quand la fréquence de commande du buzzer est de 1 KHz environ, on applique un état actif haut
    digitalWrite(emulatedMicrophoneDigitalOutput,1); // SET output HIGH
    buzzerState = 1; // update output buffer variable
  }
  else
  {
    // Quand la fréquence de comande du buzzer est élevée 31 KHz environ, on applique un état inactif bas
    digitalWrite(emulatedMicrophoneDigitalOutput,0); // SET output LOW
    buzzerState = 0; // update output buffer variable
  }
  // ---- FIN ROUTINE PERMANENTE frequencemetre ---------------------------

  // ---- MACHINE A ETATS -------------------------------------------------
  // Etats entre 0 et 8 (réalisé en fonction d'un chronogramme cyclique de commande du buzzer)
  if((state == 0) && (buzzerState == 0))
  {
    state = 1; // etat suivante
  }
  else if((state == 1) && (buzzerState == 1))
  {
    state = 2; // etat suivante
  }
  else if((state == 2) && (buzzerState == 0))
  {
    state = 3; // etat suivante
  }
  else if((state == 3) && (buzzerState == 1))
  {
    state = 4; // etat suivant
  }
  else if((state == 4) && (buzzerState == 0))
  {
    state = 5; // etat suivant
  }
  else if((state == 5) && (buzzerState == 1))
  {
    state = 6; // etat suivant
  }
  else if((state == 6) && (buzzerState == 0))
  {
    state = 7; // etat suivant
  }
  else if((state == 7) && (buzzerState == 1))
  {
    state = 8; // etat suivant
  }
  if((state == 8) && (buzzerState == 0))
  {
    state = 0; // RESET state, la boucle est bouclée
  }
  // --- Fin de la machine à états ---------------------------

  // à chaque changement d'état, on change la fréquence envoyée sur A0 de l'arduino du CSAW (broche analogique micro)
  if(newState != state) // detection d'un changement d'état
  {
    newState = state; // recopie du nouvel état dans la variable prévue à cet effet

    // CONTROLE DE LA SORTIE à fréquence controlée en fonction de l'état actuel
    if(state == 0)
    {
      tone(pinGenFreq,lowFreq); // LOW FREQUENCY = simlate the BUZZER ON
    }
    else if(state == 1)
    {
      tone(pinGenFreq, highFreq); // HIGH FREQUENCY 31.3 KHz simulate the buzzer OFF
    }
    else if(state == 2)
    {
      tone(pinGenFreq, SOSFreq); // SOS FREQUENCY during the first buzzer BEEP
    }
    else if(state == 3)
    {
      tone(pinGenFreq, highFreq); // HIGH FREQUENCY 31.3 KHz simulate the buzzer OFF
    }
    else if( state == 4 )
    {
      tone(pinGenFreq, SOSFreq);  // SOS FREQUENCY during the second buzzer BEEP
    }
    else if(state == 5)
    {
      tone(pinGenFreq, highFreq); // HIGH FREQUENCY 31.3 KHz simulate the buzzer OFF
    }
    else if(state == 6)
    {
     tone(pinGenFreq, SOSFreq);   // SOS FREQUENCY during the third buzzer BEEP
    }
    else if(state == 7)
    {
      tone(pinGenFreq, highFreq); // HIGH FREQUENCY 31.3 KHz simulate the buzzer OFF
    }
    else if(state == 8)
    {
      tone(pinGenFreq, lowFreq); // LOW FREQUENCY = simlate the BUZZER ON
    }
  }
}
