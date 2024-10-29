# GABC to MEI Neume Conversion

### MEI Neume Encoding: An Example
The following code block shows an example of the MEI encoding for the neumes in the word ("gloria"). The code shows one clef (`C3`) and two syllables ("glo" and "ria"), the first one ("glo") with one neume, and the second one ("ria") with two neumes. The image below shows the rendering of this MEI code in Verovio.
```xml
<staff n="1">
   <layer n="1">
      <clef shape="C" line="3"/>
      <syllable>
         <syl wordpos="s">glo</syl>
         <neume>
            <nc loc="2"/>
         </neume>
      </syllable>
      <syllable>
         <syl wordpos="m">ri</syl>
         <neume>
            <nc loc="5" tilt="n"/>
         </neume>
      </syllable>
      <syllable>
         <syl wordpos="t">a</syl>
         <neume>
            <nc loc="3"/>
         </neume>
         <neume>
            <nc loc="3" tilt="s"/>
            <nc loc="2" tilt="se"/>
            <nc loc="1" tilt="se"/>
        </neume>
      </syllable>
   </layer>
</staff>
```

<img width="400" alt="glo-ri-a" src="https://github.com/ECHOES-from-the-Past/GABCtoMEI/assets/13948831/8a9cca4f-1732-48f6-9057-c2c17945e6e1">

For more information on how to encode chants using MEI Neumes, please consult the [MEI Guidelines - Chapter 6](https://music-encoding.org/guidelines/v5/content/neumes.html)

### Conversion Table from GABC to MEI

|    |   Class  | Strict GABC | Neumes MEI |
|----|----------|-------------|------------|
| 1  | Square (note head)                               | lowercase characters <br/>from `a` to `m` | `<nc>` |
| 2  | Rhombus                                          | uppercase characters <br/>from `A` to `M`   | `<nc`**`tilt="se"`**`/>` |
| 3  | \[downward\] Stem <br/>&nbsp;_Right side of note_  | `v` | `<nc`**`tilt="s"`**`/>` |
| 4  | \[downward\] Stem <br/>&nbsp;_Left side of note_             | `V` | `<nc`**`tilt="n"`**`/>` (Square notation) <br/>`<nc`**`tilt="ne"`**`/>` (Aquitanian notation) |
| 5  | Liquescent (lower note)                      | `>` | `<nc`**`curve="c"`**`>`<br/>&nbsp;&nbsp;&nbsp;&nbsp;**`<liquescent/>`**<br/>`</nc>` |
| 6  | Liquescent (higher note)                        | `<` | `<nc`**`curve="a"`**`>`<br/>&nbsp;&nbsp;&nbsp;&nbsp;**`<liquescent/>`**<br/>`</nc>` |
| 7  | Oriscus                                          | `o` | `<nc>`<br/>&nbsp;&nbsp;&nbsp;&nbsp;**`<oriscus/>`**<br/>`</nc>`  |
| 8  | Quilisma                                         | `w` | `<nc>`<br/>&nbsp;&nbsp;&nbsp;&nbsp;**`<quilisma/>`**<br/>`</nc>` |
| 9 | Strophicus                                       | `s` | `<nc>`<br/>&nbsp;&nbsp;&nbsp;&nbsp;**`<strophicus/>`**<br/>`</nc>` |
| 10 | Obliqua                                          | `º` preceding first neume <br/>component of the two[^1] | `<nc`**`ligated="true"`**`/>`<br/>`<nc`**`ligated="true"`**`/>`|
| 11 | Separation of neumes                             | `/`<br/>what precedes and follows this <br/>slash are the characters representing <br/>all neume components of one neume, <br/>and the characters of all the neume <br/>components of the following neume, <br/>respectively | **`<neume>`**<br/>&nbsp;&nbsp;&nbsp;&nbsp;`<nc/>...<nc/>`<br/>**`</neume>`<br/>`<neume>`**<br/>&nbsp;&nbsp;&nbsp;&nbsp;`<nc/>...<nc/>`<br/>**`</neume>`** |
| 12 | Accidental (flat)     | `x` | `<accid`**`accid="f"`**`/>` |
| 13 | Accidental (natural)  | `y` | `<accid`**`accid="n"`**`/>` |
| 14 | Accidental (sharp)    | `#` | `<accid`**`accid="s"`**`/>` |
| 15 | Uncertain reading <br/>unclear neume components   | `r` | `<nc>`<br/>&nbsp;&nbsp;&nbsp;&nbsp;**`<unclear/>`**<br/>`</nc>` |
| 16 | Completely illegible / lacuna: <br/>we do not provide notation <br/>in the transcription                | `text()`<br/>no content inside the pair of <br/>parentheses | `<syllable>`<br/>&nbsp;&nbsp;&nbsp;&nbsp;`<syl>text</syl>`<br/>`</syllable>` <br/><br/>**no child `<neume>`** inside of `<syllable>` |

#### Notes:
There could be normal liquescents, with two tails, 
which are simply encoded as shown in entries 5 and 6 of the previous table. 
Or there could be liquescents with just one tail, for example: 
```xml
<nc curve="c" tilt="n">
 <liquescent/>
</nc>
```
which represents a liquescent that has just one tail (rather than two) in square notation; in this case, a left tail (`@tilt = n`). This neume is called "liquescent punctum" and would be encoded in our "strict" GABC as `>V`.
<!--(Only happens in square?)-->

[^1]: Not part of GABC
