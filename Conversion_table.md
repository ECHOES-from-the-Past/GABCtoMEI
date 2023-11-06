|    |   Class  | GABC | Neumes MEI |
|----|----------|------|------------|
| 1  | Square (note head)                               | lowercase characters <br/>from `a` to `m` | `<nc>` |
| 2  | Rhombus                                          | uppercase characters <br/>from `A` to `M`   | `<nc tilt="se"/>` |
| 3  | \[downward\] Stem <br/>&nbsp;_Right side of note (a virga)_  | `v` | `<nc tilt="s"/>` |
| 4  | \[downward\] Stem <br/>&nbsp;_Left side of note_             | `V` | `<nc tilt="n"/>` |
| 5  | Liquescent                                       | `~` | `<nc>`<br/>&nbsp;&nbsp;&nbsp;&nbsp;`<liquescent/>`<br/>`</nc>` |
| 6  | Liquescent (two tails down)                      | `>` | `<nc curve="c">`<br/>&nbsp;&nbsp;&nbsp;&nbsp;`<liquescent/>`<br/>`</nc>` |
| 7  | Liquescent (two tails up)                        | `<` | `<nc curve="a">`<br/>&nbsp;&nbsp;&nbsp;&nbsp;`<liquescent/>`<br/>`</nc>` |
| 8  | Oriscus                                          | `o` | `<nc>`<br/>&nbsp;&nbsp;&nbsp;&nbsp;`<oriscus/>`<br/>`</nc>`  |
| 9  | Quilisma                                         | `w` | `<nc>`<br/>&nbsp;&nbsp;&nbsp;&nbsp;`<quilisma/>`<br/>`</nc>` |
| 10 | Strophicus                                       | `s` | `<nc>`<br/>&nbsp;&nbsp;&nbsp;&nbsp;`<strophicus/>`<br/>`</nc>` |

There could be normal liquescents, with two tails, 
which are simply encoded as shown in entries 6 and 7 of the previous table. 
Or there could be liquescents with just one tail, for example: 
```xml
<nc curve="c" tilt="n">
 <liqescent/>
</nc>
```
which represents a liquescent that has just one tail (rather than two); in this case, a left tail (`@tilt = n`).
