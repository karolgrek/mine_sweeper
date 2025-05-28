# 🧩 Minesweeper

## Overview  
A fresh spin on the classic mine‑clearing puzzle.  
Choose between **two distinct game modes**, track your progress locally, and climb the high‑score ladder.

<h2>Languages and Utilities Used</h2>

- **Python 3**  
- **Pygame** (for graphics, input)

## Project Layout

| File            | Responsibility                                                         |
|-----------------|------------------------------------------------------------------------|
| `main.py`       | Launches the game, handles saves/loads, processes global input         |
| `draw.py`       | Renders everything on‑screen: board, text, buttons, effects            |
| `uncover.py`    | Core logic—flood fill, scoring, win/loss detection                     |
| `highscores.txt`| Persistent leaderboard                                                 |
| `players.txt`   | Player data in format:`name;lvl_p;score_p;mode_p;lvl_h;score_h;mode_h` |

## Game Flow (a.k.a. “Phases”)

1. **Menu**  
   - Enter a username.  
   - Press **F2** to wipe all local data (`players.txt`, `highscores.txt`).

2. **Mode Selection**  
   - Pick between two modes.  
   - Returning players see their previous stats.

3. **Board**  
   - Classic gameplay: **Left‑click** to reveal, **Right‑click** to flag.

4. **Victory / Defeat**  
   - Continue to the next level or start anew (as the same or a different user).
   
At any time, you can hit F1 to safely exit and save your progress.

## How to run

Running the game only requires Python and python Pygame library.
```bash
pip install pygame
/home/user/mines>$ python main.py
```


<p align="center">
Menu screen<br/>
<img src="https://i.imgur.com/VERdzvp.png" height="80%" width="80%" alt="Menu" />
<br />
<br />

<p align="center">Mode selection screen</p>
<p align="center">
  <img src="https://i.imgur.com/Eyq3vQC.png" width="40%" alt="Mode Selection"/>
  <img src="https://i.imgur.com/UwmPFix.png" width="40%" alt="Mode Selection Known User"/>
</p>
<p align="center"><em>Mode Selection (user logged in first time) | Mode selection (user has been already logged in)</em></p>
<br />
<br />

<p align="center">
Game screen<br/>
<img src="https://i.imgur.com/QH2r1sb.png" height="80%" width="80%" />
<br />
<br />

<p align="center">Victory / Loss screen<br/></p>
<p align="center">
  <img src="https://i.imgur.com/Az9VwWX.png" width="40%" alt="Mode Selection"/>
  <img src="https://i.imgur.com/L3ba5s4.png" width="40%" alt="Settings"/>
</p>
<br />
<br />


<!--
 ```diff
- text in red
+ text in green
! text in orange
# text in gray
@@ text in purple (and bold)@@
```
--!>
