```mermaid
graph TB

男-->女一
男-->女二
女一-->帝王
女二--後裔-->遠支
男-->實控
實控--傀儡-->帝王

classDef female fill:#ffcccc
class 女一,女二 female

classDef king fill:#ffee00
class 帝王 king

classDef far fill:#cccccc
class 遠支 far

classDef control fill:#ccffff
class 實控 control
```
