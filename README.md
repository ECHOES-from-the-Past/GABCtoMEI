# GABCtoMEI

## Encoding Guidelines

- The Aquitanian fragments have a reference line (usually drawn in red ink). We used the second line of the GABC staff (represented by the GABC `f` character) to represent this reference line.
- We used the slash `/` character to separate the neumes within a syllable.
- Features kept:
  - square shapes (lowercase letters: `a`, `b`, `c`, `d`, `e`, `f`, `g`, `h`, `i`, `j`, `k`, `l`, `m`)
  - rhombus shapes (uppercase letters: `A`, `B`, `C`, `D`, `E`, `F`, `G`, `H`, `I`, `J`, `K`, `L`, `M`)
  - square with tail on the left (marked with a `V`) or on the right (marked with a `v`)
  - special ones:
    - liquescent (`<`, `>`, `~`)
    - oriscus (`o`)
    - quilisma (`w`)
    - strophicus (`s`)
- Torculus in Aquitanian looks like a punctum followed by a clivis, but since it is a single neume, we encode it as three squares.
- Only provide a clef in GABC if there is one in the manuscript. Otherwise, we do not encode any clef and just start encoding the notes in GABC as their encoding indicates their position in the staff and has no pitch-related information.

  ![GABC_a-to-m_edited](https://github.com/martha-thomae/GABCtoMEI/assets/13948831/e313109d-5894-41f6-9c41-7ed09d9e38a9)


- Given that GABC can only display a 4-line staff, and we are working with square-notation manuscripts with 5-line staves, we decided on allowing for encoding `c5` clefs as well (even though they do not render correctly on [GABC's Transcription Tool](https://bbloomf.github.io/jgabc/transcriber.html)).
- We also decided to increase the range of the notes allowed by GABC. GABC allows to encode notes from the space below the first ledger line (represented by `a`) to the space above the fifth line (represented by `m`). We expanded this range by including some characters before `a` (these are `x`, `y`, `z`) and some characters after `m` (these are `n`, `p`, `q`). These extra characters are shown in the image below, where the red background shows the usual range covered by GABC and the extended system is shown by the characters in the blue background.
  
  ![GABC_x-to-q_edited](https://github.com/martha-thomae/GABCtoMEI/assets/13948831/7e510f0e-50af-4dbc-841b-edb10ee27250)
