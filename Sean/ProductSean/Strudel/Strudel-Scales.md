'scale('C:major')' # major	The standard Major scale (Ionian mode).	.
'.scale('A:minor')' # minor	The standard Natural Minor scale (Aeolian mode).	
'.scale('C:harmonicMinor')' # harmonicMinor	Natural minor with a raised 7th degree.	
'.scale('G:melodicMinor')' # melodicMinor	Minor scale with raised 6th and 7th ascending, natural minor descending.	
ionian	# Major (1st degree)	Same as Major scale.
dorian	# Minor (2nd degree)	Minor with a raised 6th.
phrygian	# Minor (3rd degree)	Minor with a flat 2nd.
lydian	# Major (4th degree)	Major with a raised 4th.
mixolydian	# Major (5th degree)	Major with a flat 7th.
aeolian	# Minor (6th degree)	Same as Natural Minor scale.
locrian	# Diminished (7th degree)	Flat 2nd and flat 5th (unstable).
'.scale('D:majorPent')' # majorPent	Major scale without the 4th and 7th degrees.	
'.scale('E:minorPent')' # minorPent	Natural minor scale without the 2nd and 6th degrees.	
'.scale('A:blues')' # blues	Minor pentatonic with an added flat 5th (the "blue" note).	
whole (wholetone)	A six-note scale built entirely on whole steps.
chromatic	# All twelve notes in an octave.
augmented	# A six-note scale built by alternating minor thirds and half steps.
diminished (dim)	# An eight-note scale alternating whole and half steps.
superLocrian	# Also known as the Altered scale, the 7th mode of the melodic minor.
bebopMajor	# Major scale with an added chromatic passing tone.
bebopMinor	# Minor scale with an added chromatic passing tone.
halfWhole	# Diminished scale alternating half steps and whole steps.
majorBebop	# An eight-note scale used in jazz improvisation.
ritusen	# Traditional Japanese pentatonic scale.	
hirajoshi	# Traditional Japanese pentatonic scale.	
iwato	# Traditional Japanese pentatonic scale.	
chinese	# Common Chinese pentatonic scale.	
egyptian	# African/Middle Eastern-sounding pentatonic scale.	
indian	# Broad term for certain Indian-inspired scales.	
prometheus	# An unusual six-note scale.	
scriabin	# A symmetrical, non-diatonic scale.

Use these scale names with the .scale('RootNote:ScaleName') function in your Strudel code (e.g., 'C4:major').

1. Major and Minor Scales

| Scale Name | Code Example | Description |
| :--- | :--- | :--- |
| major | n("0 1 2 3").scale('C4:major') | The standard Major scale (Ionian mode). |
| minor | n("0 1 2 3").scale('A4:minor') | The standard Natural Minor scale (Aeolian mode). |
| harmonicMinor | n("0 1 2 3").scale('C4:harmonicMinor') | Natural minor with a raised 7th degree. |
| melodicMinor | n("0 1 2 3").scale('G4:melodicMinor') | Minor with raised 6th and 7th ascending. |

2. Modal Scales (The 7 Modes)

| Mode Name | Code Example | Description |
| :--- | :--- | :--- |
| ionian | n("0 1 2 3").scale('C4:ionian') | Same as Major scale (1st mode). |
| dorian | n("0 1 2 3").scale('D4:dorian') | Minor scale with a raised 6th (2nd mode). |
| phrygian | n("0 1 2 3").scale('E4:phrygian') | Minor scale with a flat 2nd (3rd mode). |
| lydian | n("0 1 2 3").scale('F4:lydian') | Major scale with a raised 4th (4th mode). |
| mixolydian | n("0 1 2 3").scale('G4:mixolydian') | Major scale with a flat 7th (5th mode). |
| aeolian | n("0 1 2 3").scale('A4:aeolian') | Same as Natural Minor scale (6th mode). |
| locrian | n("0 1 2 3").scale('B4:locrian') | Diminished scale with flat 2nd and 5th (7th mode). |

3. Pentatonic and Blues

| Scale Name | Code Example | Description |
| :--- | :--- | :--- |
| majorPent | n("0 1 2 3").scale('D4:majorPent') | Major scale without the 4th and 7th degrees. |
| minorPent | n("0 1 2 3").scale('E4:minorPent') | Natural minor scale without the 2nd and 6th degrees. |
| blues | n("0 1 2 3").scale('A4:blues') | Minor pentatonic with an added flat 5th ("blue" note). |

4. Symmetric and Jazz Scales

| Scale Name | Code Example | Description |
| :--- | :--- | :--- |
| whole or wholetone | n("0 1 2 3").scale('C4:whole') | A six-note scale built entirely on whole steps. |
| chromatic | n("0 1 2 3").scale('C4:chromatic') | All twelve notes in an octave. |
| augmented | n("0 1 2 3").scale('C4:augmented') | Alternating minor thirds and half steps (six-note). |
| diminished or dim | n("0 1 2 3").scale('C4:diminished') | Alternating whole and half steps (eight-note). |
| superLocrian | n("0 1 2 3").scale('C4:superLocrian') | Also known as the Altered scale, the 7th mode of the melodic minor. |
| bebopMajor | n("0 1 2 3").scale('C4:bebopMajor') | Major scale with an added chromatic passing tone. |
| bebopMinor | n("0 1 2 3").scale('C4:bebopMinor') | Minor scale with an added chromatic passing tone. |
| halfWhole | n("0 1 2 3").scale('C4:halfWhole') | Diminished scale alternating half steps and whole steps. |
| majorBebop | n("0 1 2 3").scale('C4:majorBebop') | An eight-note scale used in jazz improvisation. |

5. Global and Exotic Scales

| Scale Name | Code Example | Description |
| :--- | :--- | :--- |
| ritusen | n("0 1 2 3").scale('C4:ritusen') | Traditional Japanese pentatonic scale. |
| hirajoshi | n("0 1 2 3").scale('C4:hirajoshi') | Traditional Japanese pentatonic scale. |
| iwato | n("0 1 2 3").scale('C4:iwato') | Traditional Japanese pentatonic scale. |
| chinese | n("0 1 2 3").scale('C4:chinese') | Common Chinese pentatonic scale. |
| egyptian | n("0 1 2 3").scale('C4:egyptian') | African/Middle Eastern-sounding pentatonic scale. |
| indian | n("0 1 2 3").scale('C4:indian') | Indian-inspired scale. |
| prometheus | n("0 1 2 3").scale('C4:prometheus') | An unusual six-note scale. |
| scriabin | n("0 1 2 3").scale('C4:scriabin') | Symmetrical, non-diatonic scale. |

Root Note Examples (Major & Minor)

To show how the root note and octave change the scale, here are examples for every letter (C4 is the middle C octave).

| Root Note | Major Example | Minor Example |
| :--- | :--- | :--- |
| C | n("0 1 2").scale('C4:major') | n("0 1 2").scale('C4:minor') |
| D | n("0 1 2").scale('D4:major') | n("0 1 2").scale('D4:minor') |
| E | n("0 1 2").scale('E4:major') | n("0 1 2").scale('E4:minor') |
| F | n("0 1 2").scale('F4:major') | n("0 1 2").scale('F4:minor') |
| G | n("0 1 2").scale('G4:major') | n("0 1 2").scale('G4:minor') |
| A | n("0 1 2").scale('A4:major') | n("0 1 2").scale('A4:minor') |
| B | n("0 1 2").scale('B4:major') | n("0 1 2").scale('B4:minor') |
