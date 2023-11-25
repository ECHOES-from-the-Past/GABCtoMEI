|    |   Class  | Strict GABC | Neumes MEI |
|----|----------|-------------|------------|
| 1  | Square (note head)                               | lowercase characters <br/>from `a` to `m` | `<nc>` |
| 2  | Rhombus                                          | uppercase characters <br/>from `A` to `M`   | `<nc`**`tilt="se"`**`/>` |
| 3  | \[downward\] Stem <br/>&nbsp;_Right side of note_  | `v` | `<nc`**`tilt="s"`**`/>` |
| 4  | \[downward\] Stem <br/>&nbsp;_Left side of note_             | `V` | `<nc`**`tilt="n"`**`/>` (Square notation) <br/>`<nc`**`tilt="ne"`**`/>` (Aquitanian notation) |
| 5  | Liquescent                                       | `~` | `<nc>`<br/>&nbsp;&nbsp;&nbsp;&nbsp;**`<liquescent/>`**<br/>`</nc>`<br/>depending on the melodic contour of <br/>the neume, add a `@curve` attribute  |
|    | (Rising melody)                    | Example `gh~`  | `<nc`**`curve="a"`**`/>`<br/>`<nc>`<br/>&nbsp;&nbsp;&nbsp;&nbsp;**`<liquescent/>`**<br/>`</nc>` |
|    | (Rising melody <br/>with stem `V`) | Example `ghV~` | `<nc/>`<br/>`<nc tilt="ne"`**`curve="c"`**`>`<br/>&nbsp;&nbsp;&nbsp;&nbsp;**`<liquescent/>`**<br/>`</nc>` |
|    | (Falling melody)                   | Example `hg~`  | `<nc/>`<br/>`<nc`**`curve="c"`**`>`<br/>&nbsp;&nbsp;&nbsp;&nbsp;**`<liquescent/>`**<br/>`</nc>` |
| 6  | Liquescent (two tails down)                      | `>` | `<nc`**`curve="c"`**`>`<br/>&nbsp;&nbsp;&nbsp;&nbsp;**`<liquescent/>`**<br/>`</nc>` |
| 7  | Liquescent (two tails up)                        | `<` | `<nc`**`curve="a"`**`>`<br/>&nbsp;&nbsp;&nbsp;&nbsp;**`<liquescent/>`**<br/>`</nc>` |
| 8  | Oriscus                                          | `o` | `<nc>`<br/>&nbsp;&nbsp;&nbsp;&nbsp;**`<oriscus/>`**<br/>`</nc>`  |
| 9  | Quilisma                                         | `w` | `<nc>`<br/>&nbsp;&nbsp;&nbsp;&nbsp;**`<quilisma/>`**<br/>`</nc>` |
| 10 | Strophicus                                       | `s` | `<nc>`<br/>&nbsp;&nbsp;&nbsp;&nbsp;**`<strophicus/>`**<br/>`</nc>` |
| 11 | Obliqua                                          | `º` preceding first neume <br/>component of the two[^1] | `<nc`**`ligated="true"`**`/>`<br/>`<nc`**`ligated="true"`**`/>`|
| 12 | Separation of neumes                             | `/`<br/>what precedes and follows this <br/>slash are the characters representing <br/>all neume components of one neume, <br/>and the characters of all the neume <br/>components of the following neume, <br/>respectively | **`<neume>`**<br/>&nbsp;&nbsp;&nbsp;&nbsp;`<nc/>...<nc/>`<br/>**`</neume>`<br/>`<neume>`**<br/>&nbsp;&nbsp;&nbsp;&nbsp;`<nc/>...<nc/>`<br/>**`</neume>`** |
| 13 | Accidental (flat)     | `x` | `<accid`**`accid="f"`**`/>` |
| 14 | Accidental (natural)  | `y` | `<accid`**`accid="n"`**`/>` |
| 15 | Accidental (sharp)    | `#` | `<accid`**`accid="s"`**`/>` |
| 16 | Unclear               | `r` | **`<unclear>`**<br/>&nbsp;&nbsp;&nbsp;&nbsp;`<nc/>`<br/>**`</unclear>`** |


There could be normal liquescents, with two tails, 
which are simply encoded as shown in entries 6 and 7 of the previous table. 
Or there could be liquescents with just one tail, for example: 
```xml
<nc curve="c" tilt="n">
 <liquescent/>
</nc>
```
which represents a liquescent that has just one tail (rather than two); in this case, a left tail (`@tilt = n`). This would be encoded in our "strict" GABC as `>V`.

[^1]: Not part of GABC
