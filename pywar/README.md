# Overview

This repository contains a complete simulated implementation of the classic card game "War".

> **Note:** This description was written using GitHub Copilot in Agent mode to verify its capabilities.

### What is War?

War is a simplified card game where two players compete using a standard 52-card deck. The game is entirely based on chance, making it perfect for automated simulation. Here's how it works:

#### Game Setup
- A deck of 52 cards (represented as integers 1-52) is shuffled randomly
- Cards are dealt evenly between two players in alternating fashion
- Each player receives 26 cards in their personal stack

#### Gameplay
- Players simultaneously reveal their top card each round
- The player with the higher-valued card wins both cards
- Won cards are added to the winner's scoring pile
- The game continues until all cards have been played

#### Winning Conditions
- The player with the most cards in their scoring pile wins
- In case of a tie, the winner is determined by who holds the highest-value card in their scoring pile

### Features

This simulator includes:
- **Asynchronous gameplay** with visual round-by-round progression
- **Automatic card shuffling and dealing** ensuring fair distribution
- **Real-time game state tracking** showing each player's remaining cards
- **Comprehensive scoring system** with tiebreaker logic
- **Clean object-oriented design** using Python dataclasses
- **Error handling** for graceful game termination

The game runs automatically from start to finish, displaying each round's results and providing a complete play-by-play experience of this classic card game. 

# Environment setup:
Made on macOS. The following pre-requisites must be set in place:
* git
* python 3.12+ with virtualenv (recommended, could work just as well with system Python3 and system libraries but it's a *meh* setup)

  Mandatory add-ons:
  * `uv` project manager
  
  Recommended add-ons:
  * pyenv - setup local env and install packages into it

> **WARNING**: I'm struggling currently to make `uv` work seamlessly together with `pyenv`. I read that various sources recommend replace'ing `pyenv` with `uv`, however that would break many of my current work patterns at the current stage, so I'm not doing it yet.
>
> Current workaround is to add always `--active` flag for any package installation / upgrade / build activities or set flag to use system python (as uv treats any pyenv shim as a System Python).
>
> Work on a real solution is in progress.

Setup steps:
1. `git clone` of the repository,
2. Install the libraries using `uv install`.
