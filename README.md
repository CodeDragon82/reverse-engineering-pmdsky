# Documenting the reverse-engineering process for *Pokemon Mystery Dungeon: Explorers of Sky*

## Introduction

In this project, I will attempt reverse-engineer one of my favourite childhood DS games: *Pokémon Mystery Dungeon: Explorers of Sky* and document the process. The reverse-engineering process will primarily focus on static analysis of the ARM9 binary using the tool Ghidra. I'm also using my custom Ghidra extension, [Ndsware](https://github.com/CodeDragon82/nds-ware), to load the main ARM9 code and overlay sections into Ghidra.

A big reason for choosing to reverse-engineer *Pokémon Mystery Dungeon: Explorers of Sky* rather than some other DS games, is because of the instruction set used. The Nintendo DS is an ARMv5T (32-bit) architecture, which supports both ARM (32-bit) and Thumb (16-bit) instructions. Many DS games switch between instruction sets for different functions. This can be difficult for reverse-engineering, because Ghidra’s decompiler often struggles to correctly identify which instruction set to use at any given time. Fortunately, *Pokémon Mystery Dungeon: Explorers of Sky* uses only the ARM instruction set, which makes Ghidra’s auto-analysis and decompilation significantly more reliable.

Due to legal reasons, I will not provide the `.nds` ROM for this game, nor do I encourage pirating the game. If you own a legitimate copy, there are many tutorials online that explain how to extract the ROM yourself. This documentation will not cover the extraction process.

I'm aware that others have already reverse-engineered and documented various aspects of this game. However, the goal of this documentation is to walk the reader through the process of reverse-engineering a game like this. This documentation will also highlight challenges and discuss techniques used to overcome them.

This research is currently a work in progress, so I'll be continuously adding to it and amend mistakes as I discover new information. It's worth noting that I'm new to reversing ARM binaries and DS games, so I'm likely to make bad assumptions from time to time. If I get anything wrong please feel free to reach out (via GitHub Issues) and let me know.
