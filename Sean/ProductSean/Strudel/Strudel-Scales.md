# Strudel Scales & Root Notes

Use these scale names with the `.scale('RootNote:ScaleName')` function in your Strudel code (e.g., 'C4:major').

## 1. Major and Minor Scales

| Scale Name | Code Example | Description | When to Use |
| :--- | :--- | :--- | :--- |
| **major** | `n("0 1 2 3").scale('C4:major')` | The standard Major scale (Ionian mode). | **Best for happy, bright, and stable melodies.** |
| **minor** | `n("0 1 2 3").scale('A4:minor')` | The standard Natural Minor scale (Aeolian mode). | **Best for sad, dark, and simple moods.** |
| **harmonicMinor** | `n("0 1 2 3").scale('C4:harmonicMinor')` | Natural minor with a raised 7th degree. | **Best for Middle-Eastern, dramatic, or suspenseful melodies** (due to the large gap between the 6th and 7th notes). |
| **melodicMinor** | `n("0 1 2 3").scale('G4:melodicMinor')` | Minor with raised 6th and 7th ascending. | **Best for Jazz fusion, complex chord progressions, and modern harmony.** |

## 2. Modal Scales (The 7 Modes)

| Mode Name | Code Example | Description | When to Use |
| :--- | :--- | :--- | :--- |
| **ionian** | `n("0 1 2 3").scale('C4:ionian')` | Same as Major scale (1st mode). | **Pop and Folk:** Use for simple, bright, and familiar melodies. |
| **dorian** | `n("0 1 2 3").scale('D4:dorian')` | Minor scale with a raised 6th (2nd mode). | **Blues and Funk:** Use for a minor, melancholic feel that is less dark than the natural minor. Very common in jazz and rock. |
| **phrygian** | `n("0 1 2 3").scale('E4:phrygian')` | Minor scale with a flat 2nd (3rd mode). | **Flamenco and Metal:** Use for an exotic, Spanish, or intense, dark sound (often heard in heavy metal solos). |
| **lydian** | `n("0 1 2 3").scale('F4:lydian')` | Major scale with a raised 4th (4th mode). | **Film Scores and Dream Pop:** Use for a floating, mystical, or bright, unresolved, "heavenly" sound. |
| **mixolydian** | `n("0 1 2 3").scale('G4:mixolydian')` | Major scale with a flat 7th (5th mode). | **Rock and Funk:** Use for a bluesy, dominant, "gritty" major sound. It sounds great over a 7th chord. |
| **aeolian** | `n("0 1 2 3").scale('A4:aeolian')` | Same as Natural Minor scale (6th mode). | **Pop and Trance:** Use for classic, universally recognized minor-key sadness. |
| **locrian** | `n("0 1 2 3").scale('B4:locrian')` | Diminished scale with flat 2nd and 5th (7th mode). | **Atonal or Experimental:** Rarely used for melody due to its instability, but great for creating tension or dissonant textures. |

## 3. Pentatonic and Blues

| Scale Name | Code Example | Description | When to Use |
| :--- | :--- | :--- | :--- |
| **majorPent** | `n("0 1 2 3").scale('D4:majorPent')` | Major scale without the 4th and 7th degrees. | **Best for simple, memorable, and safe melodies.** |
| **minorPent** | `n("0 1 2 3").scale('E4:minorPent')` | Natural minor scale without the 2nd and 6th degrees. | **Best for simple, driving, and rock-oriented basslines/leads.** |
| **blues** | `n("0 1 2 3").scale('A4:blues')` | Minor pentatonic with an added flat 5th ("blue" note). | **Best for soulful, expressive, and improvisational blues/rock leads.** |

## 4. Symmetric and Jazz Scales

| Scale Name | Code Example | Description | When to Use |
| :--- | :--- | :--- | :--- |
| **whole** or **wholetone** | `n("0 1 2 3").scale('C4:whole')` | A six-note scale built entirely on whole steps. | **Use for creating ambiguous, dreamlike, or suspenseful textures.** |
| **chromatic** | `n("0 1 2 3").scale('C4:chromatic')` | All twelve notes in an octave. | **Use to bypass scale constraints for complex or dissonant patterns.** |
| **augmented** | `n("0 1 2 3").scale('C4:augmented')` | Alternating minor thirds and half steps (six-note). | **Use for unsettling, surreal, or dramatic harmonic movement.** |
| **diminished** or **dim** | `n("0 1 2 3").scale('C4:diminished')` | Alternating whole and half steps (eight-note). | **Use for intense suspense, horror scores, or complex jazz runs.** |
| **superLocrian** | `n("0 1 2 3").scale('C4:superLocrian')` | Also known as the Altered scale, the 7th mode of the melodic minor. | **Use for creating tension over a dominant 7th chord in jazz/funk.** |
| **bebopMajor** | `n("0 1 2 3").scale('C4:bebopMajor')` | Major scale with an added chromatic passing tone. | |
| **bebopMinor** | `n("0 1 2 3").scale('C4:bebopMinor')` | Minor scale with an added chromatic passing tone. | |
| **halfWhole** | `n("0 1 2 3").scale('C4:halfWhole')` | Diminished scale alternating half steps and whole steps. | |
| **majorBebop** | `n("0 1 2 3").scale('C4:majorBebop')` | An eight-note scale used in jazz improvisation. | |

## 5. Global and Exotic Scales

| Scale Name | Code Example | Description | When to Use |
| :--- | :--- | :--- | :--- |
| **ritusen** | `n("0 1 2 3").scale('C4:ritusen')` | Traditional Japanese pentatonic scale. | **Use for delicate, ancient, or Eastern-inspired melodies.** |
| **hirajoshi** | `n("0 1 2 3").scale('C4:hirajoshi')` | Traditional Japanese pentatonic scale. | **Use for a darker, more dramatic Japanese sound.** |
| **iwato** | `n("0 1 2 3").scale('C4:iwato')` | Traditional Japanese pentatonic scale. | **Use for a darker, more dramatic Japanese sound.** |
| **chinese** | `n("0 1 2 3").scale('C4:chinese')` | Common Chinese pentatonic scale. | **Use for simple, memorable, and often bright Chinese music styles.** |
| **egyptian** | `n("0 1 2 3").scale('C4:egyptian')` | African/Middle Eastern-sounding pentatonic scale. | **Use for driving, exotic, or desert-like music.** |
| **indian** | `n("0 1 2 3").scale('C4:indian')` | Indian-inspired scale. | **Use for complex, microtonal-sounding Indian melodies.** |
| **prometheus** | `n("0 1 2 3").scale('C4:prometheus')` | An unusual six-note scale. | **Use for highly dissonant or modernist sounds.** |
| **scriabin** | `n("0 1 2 3").scale('C4:scriabin')` | Symmetrical, non-diatonic scale. | **Use for impressionistic, shimmering, or surreal compositions.** |

***

## Root Note Examples (Major & Minor)

To show how the root note and octave change the scale, here are examples for every letter (C4 is the middle C octave).

| Root Note | Major Example | Minor Example |
| :--- | :--- | :--- |
| **C** | `n("0 1 2").scale('C4:major')` | `n("0 1 2").scale('C4:minor')` |
| **D** | `n("0 1 2").scale('D4:major')` | `n("0 1 2").scale('D4:minor')` |
| **E** | `n("0 1 2").scale('E4:major')` | `n("0 1 2").scale('E4:minor')` |
| **F** | `n("0 1 2").scale('F4:major')` | `n("0 1 2").scale('F4:minor')` |
| **G** | `n("0 1 2").scale('G4:major')` | `n("0 1 2").scale('G4:minor')` |
| **A** | `n("0 1 2").scale('A4:major')` | `n("0 1 2").scale('A4:minor')` |
| **B** | `n("0 1 2").scale('B4:major')` | `n("0 1 2").scale('B4:minor')` |
