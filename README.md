# GABCtoMEI

In addition to the GABC specifications (that can be found [here](https://gregorio-project.github.io/gabc/index.html)), we followed the next encoding guidelines to encode all the features necessary for converting GABC files into MEI Neumes files. This conversion is done with the [gabc-tokens_to_mei-elements.py](https://github.com/martha-thomae/GABCtoMEI/blob/main/gabc-tokens_to_mei-elements.py) script.

## Encoding Guidelines

- The Aquitanian fragments have a reference line (usually drawn in red ink and sometimes with drypoint, which can be read as D, F, G, A, or B according to the mode of the chant). We used the second line of the GABC staff (represented by the GABC `f` character) to represent this reference line.
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
- Torculus in Aquitanian looks like a punctum followed by a clivis ![image](https://github.com/martha-thomae/GABCtoMEI/assets/13948831/72005277-2136-4102-b3a4-d003bd013c4d), but since it is a single neume, we encode it as a single neume consisting of three squares.
  
  **Example:** A syllable with just one torculus that starts in the second line (`f`), moves up a third (`h`), and back down a third (`f`).
  -  This torculus would be encoded as `(fhf)`, which is a single neume
  -  And not as `(f/hVf)`, because in this case the glyph would be composed of two neumes, as indicated by the `/` (see bullet point two), with these two neumes being a square `f` and a clivis `hVf`

- Only provide a clef in GABC if there is one in the manuscript. Otherwise, we do not encode any clef and just start encoding the notes in GABC as their encoding indicates their position in the staff and has no pitch-related information.

  ![GABC_a-to-m_edited](https://github.com/martha-thomae/GABCtoMEI/assets/13948831/e313109d-5894-41f6-9c41-7ed09d9e38a9)


- Given that GABC can only display a 4-line staff, and we are working with square-notation manuscripts with 5-line staves, we decided on allowing for encoding `c5` clefs as well (even though they do not render correctly on [GABC's Transcription Tool](https://bbloomf.github.io/jgabc/transcriber.html)).
- We also decided to increase the range of the notes allowed by GABC. GABC allows to encode notes from the space below the first ledger line (represented by `a`) to the space above the fifth line (represented by `m`). We expanded this range by including some characters before `a` (these are `x`, `y`, `z`) and some characters after `m` (these are `n`, `p`, `q`). These extra characters are shown in the image below, where the red background shows the usual range covered by GABC and the extended system is shown by the characters in the blue background. The extra characters would not be rendered on the [GABC Transcription Tool](https://bbloomf.github.io/jgabc/transcriber.html), but they are useful to encode a wider range than the one currently allowed.
  
  ![GABC_x-to-q_edited](https://github.com/martha-thomae/GABCtoMEI/assets/13948831/7e510f0e-50af-4dbc-841b-edb10ee27250)

## Conversion Process (GABC to MEI)
To use the Python `gabc-tokens_to_mei-elements.py` script, you need to provide the following information:
- input file (with extension `.txt`)
- output file (with extension `.mei`)
- type of notation (`square` or `aquitanian` using the flag `-notation`), if no value is provided, the program will use `aquitanian` notation as the default

These are a few examples of how to run the program:

- For square notation:
  
  ```
  python3 gabc-tokens_to_mei-elements.py <input_file_name>.txt <output_file_name>.mei -notation square
  ```

- For aquitanian notation:
  ```
  python3 gabc-tokens_to_mei-elements.py <input_file_name>.txt <output_file_name>.mei -notation aquitanian
  ```

  or 
  ```
  python3 gabc-tokens_to_mei-elements.py <input_file_name>.txt <output_file_name>.mei
  ```

The program will produce two types of MEI files:

1. One that encodes the location of the notes in the staff using `@loc` (see the attribute [description](https://music-encoding.org/guidelines/v5/attribute-classes/att.staffLoc.html) and its [values](https://music-encoding.org/guidelines/v5/data-types/data.STAFFLOC.html)).
2. And one that encodes the final file by substituting the `@loc` value with:
   1. the melodic intervals (`@intm`), in the case of Aquitanian notation
   2. the pitch (with `@pname` and `@oct`), in the case of square notation
