# GABCtoMEI

In addition to the GABC specifications (that can be found [here](https://gregorio-project.github.io/gabc/index.html)), we followed the next encoding guidelines to encode all the features necessary for converting GABC files into MEI Neumes files. This conversion is done with the [gabc-tokens_to_mei-elements.py](https://github.com/martha-thomae/GABCtoMEI/blob/main/gabc-tokens_to_mei-elements.py) script.

## Encoding Guidelines

- The Aquitanian fragments have a reference line (usually drawn in red ink and sometimes with drypoint, which can be read as D, F, G, A, or B according to the mode of the chant). We used the second line of the GABC staff (represented by the GABC `f` character) to represent this reference line.
- We restricted the characters used (we did not use separation bars, text formatting or special characters, custos, “special” spacing, or accents and attachments).
- We used the slash `/` character to separate the neumes within a syllable ("neumatic cut"). And we used the regular space ` ` character to separate the words in the chant ("word space"). We did consider any other kind of "space"-related characters (no `@` to indicate connection between notes, no exclamation mark `!` to indicate no connection between the notes, no double slash `//` to indicate large neumatic cuts, no half-space `/0` character, and no mix of slash with bracketed numbers `/[factor]` to scale the neumatic cut).
  
  **IMPORTANT:** Single notes that are part of the same neume are regarded as graphically joined. Only long tails are signaled, not the pen-strokes that join two squares within a neume.

- Features kept:
  - Square shapes (lowercase letters: `a`, `b`, `c`, `d`, `e`, `f`, `g`, `h`, `i`, `j`, `k`, `l`, `m`)
  - Rhombus shapes (uppercase letters: `A`, `B`, `C`, `D`, `E`, `F`, `G`, `H`, `I`, `J`, `K`, `L`, `M`)
  - Square with tail on the left (marked with a `V`) or on the right (marked with a `v`)
    - **Note:** Because we were explicit about the presence of stems at the beginning (`V`) and end (`v`) of a neume, we did not use the `@` character to indicate the "abscence" of a stem.
  - Accidentals (flats with `x`, naturals with `y`, and sharps with `#`)

  - Special ones:
    - Oriscus (`o`)
    - Quilisma (`w`)
    - Strophicus (`s`)
    - Liquescent (`<`, `>`, `~`)
      - A liquescent epiphonus (i.e., a neume component with a liquescent indicating a second, higher note) is represented by `<`. In MEI this would be represented with a `@curve=a` in the neume component `<nc>`, plus a child `<liquescent>`. Additionally, the `<nc>` is classified as an *epiphonus* by including a `@type = epiphonus`.
      - A liquescent cephalicus (i.e., a neume component with a liquescent indicating a second, lower note) is represented by `>`. In MEI this would be represented with a `@curve=c` in the neume component `<nc>`, plus a child `<liquescent>`. Additionally, the `<nc>` is classified as a *cephalicus* by including a `@type = cephalicus`.
      - On the other hand, if we want to represent a liquescent virga, one needs to add a `V` or `v` to the liquescent symbol `>` to indicate the type of virga (`V` for a virga with downward stem at the left or `v` for a virga with a downward stem at the right).[^1] In this case, the MEI encoding does not have a `@type = epiphonus` or `@type = cephalicus` as we don't know whether the liquescent represents a higher or lower note, but we still have `@curve = c` (as the liquescent virga always has a clockwise curve), with an additional `@tilt = n` for a left downward stem or `@tilt = s` for a right downward stem.
- Features added:
  - Use `º` as a prefix to mark the first neume component of the pair of an obliqua ligature.

    **Example:** `(gVºhfj)`,  which means that from the four neume components in this neume (`gV`, `h`, `f`, and `j`), the two neume components in the middle, `h` and `f`, are ligated in oblique motion (in MEI this would be equivalent to both neume components `<nc>` having an attribute `@ligated = obliqua`).



  The GABC encoding of the previously mentioned features (square, rhombus, virga, oriscus, quilisma, strophicus, liquescent, obliqua ligatures, and accidentals) and others (neume groupings, uncertain readings, and lacunas) and their corresponding MEI Neumes encoding is given in the [Conversion Table from GABC to MEI Neumes](./README_conversion_table.md).



- Torculus in Aquitanian looks like a punctum followed by a clivis ![torculus](https://github.com/martha-thomae/GABCtoMEI/tree/main/images/torculusAsTorculus.png), but since it is a single neume, we encode it as a single neume consisting of three squares with the upper pitch having a tail on the left.
  
  **Example:** A syllable with just one torculus that starts in the second line (`f`), moves up a third (`h`) with a stem on the left pointing to a 'north-east' direction (`hV`), and back down a third (`f`).
  -  This torculus would be encoded as `(fhVf)`, which is a single neume
  -  And not as `(f/hVf)`, because in this case the glyph would be composed of two neumes, as indicated by the `/` (see bullet point two), with these two neumes being a square `f` and a clivis `hVf`

- Only provide a clef in GABC if there is one in the manuscript. Otherwise, we do not encode any clef and just start encoding the notes in GABC as their encoding indicates their position in the staff and has no pitch-related information.

  ![GABC_a-to-m_edited](https://github.com/martha-thomae/GABCtoMEI/tree/main/images/GABC_a-to-m_edited.png)


- Given that GABC can only display a 4-line staff, and we are working with square-notation manuscripts with 5-line staves, we decided on allowing for encoding `c5` clefs as well (even though they do not render correctly on [GABC's Transcription Tool](https://bbloomf.github.io/jgabc/transcriber.html)).
- We also decided to increase the range of the notes allowed by GABC. GABC allows to encode notes from the space below the first ledger line (represented by `a`) to the space above the fifth line (represented by `m`). We expanded this range by including some characters before `a` (these are `t`, `u`, `z`) and some characters after `m` (these are `n`, `p`, `q`). These extra characters are shown in the image below, where the red background shows the usual range covered by GABC and the extended system is shown by the characters in the blue background. The extra characters would not be rendered on the [GABC Transcription Tool](https://bbloomf.github.io/jgabc/transcriber.html), but they are useful to encode a wider range than the one currently allowed.
  
  ![extended_gabc_scale](https://github.com/martha-thomae/GABCtoMEI/tree/main/images/GABC_x-to-q_edited.png)


## Conversion Process (GABC to MEI)
To use the Python `gabc-tokens_to_mei-elements.py` script, you need to provide the following information:
- Input file name (with extension `.txt`), saved in the _GABC_infiles_ folder
- Output file name (with extension `.mei`), which will be saved in the _MEI_outfiles_ folder
- Type of notation (`square` or `aquitanian` using the flag `-notation`), if no value is provided, the program will use `aquitanian` notation as the default

These are a few examples of how to run the program, provided that the input GABC file is in the **GABC_infiles** folder:

- For square notation:
  
  ```
  python3 gabc-tokens_to_mei-elements.py GABC_infiles/<input_file_name>.txt MEI_outfiles/<output_file_name>.mei -notation square
  ```

- For Aquitanian notation:
  ```
  python3 gabc-tokens_to_mei-elements.py GABC_infiles/<input_file_name>.txt MEI_outfiles/<output_file_name>.mei -notation aquitanian
  ```

  or 
  ```
  python3 gabc-tokens_to_mei-elements.py GABC_infiles/<input_file_name>.txt MEI_outfiles/<output_file_name>.mei
  ```

The program will produce two types of MEI files:

1. One that encodes the location of the notes in the staff using `@loc` (see the attribute [description](https://music-encoding.org/guidelines/v5/attribute-classes/att.staffLoc.html) and its [values](https://music-encoding.org/guidelines/v5/data-types/data.STAFFLOC.html)). These files are found in the **MEI_intermedfiles** folder within the **MEI_outfiles**.
2. And one that encodes the final file by substituting the `@loc` value by:
   1. The pitch (with `@pname` and `@oct`), in the case of square notation.
   2. Recomputing the location value (`@loc`) based on a reference line (`<staffDef lines="1">`), in the case of Aquitanian notation.

   These output files for square and Aquitanian notation can be found in the **MEI_outfiles** folder.


[^1]: The liquescent symbol used is `>` as liquescent virgas are always drawn with a clockwise curve (`@curve = c` in MEI).