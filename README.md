# Documenting the reverse-engineering process for *Pokemon Mystery Dungeon: Explorers of Sky*

## Introduction

In this project, I will attempt reverse-engineer one of my favourite childhood DS games: *Pokémon Mystery Dungeon: Explorers of Sky* and document the process. The reverse-engineering process will primarily focus on static analysis of the ARM9 binary using the tool Ghidra. I'm also using my custom Ghidra extension, [Ndsware](https://github.com/CodeDragon82/nds-ware), to load the main ARM9 code and overlay sections into Ghidra.

A big reason for choosing to reverse-engineer *Pokémon Mystery Dungeon: Explorers of Sky* rather than some other DS games, is because of the instruction set used. The Nintendo DS is an ARMv5T (32-bit) architecture, which supports both ARM (32-bit) and Thumb (16-bit) instructions. Many DS games switch between instruction sets for different functions. This can be difficult for reverse-engineering, because Ghidra’s decompiler often struggles to correctly identify which instruction set to use at any given time. Fortunately, *Pokémon Mystery Dungeon: Explorers of Sky* uses only the ARM instruction set, which makes Ghidra’s auto-analysis and decompilation significantly more reliable.

Due to legal reasons, I will not provide the `.nds` ROM for this game, nor do I encourage pirating the game. If you own a legitimate copy, there are many tutorials online that explain how to extract the ROM yourself. This documentation will not cover the extraction process.

I'm aware that others have already reverse-engineered and documented various aspects of this game. However, the goal of this documentation is to walk the reader through the process of reverse-engineering a game like this. This documentation will also highlight challenges and discuss techniques used to overcome them.

This research is currently a work in progress, so I'll be continuously adding to it and amend mistakes as I discover new information. It's worth noting that I'm new to reversing ARM binaries and DS games, so I'm likely to make bad assumptions from time to time. If I get anything wrong please feel free to reach out (via GitHub Issues) and let me know.

## Prerequisite Knowledge

To ensure that this documentation doesn't require a book worth of notes, I will be assumed that you have the following prerequisite knowledge:

- A decent understanding of how to use Ghidra.
- Familiarity with C consepts such as structs, enums, functions, pointers, global variables/constants, etc.
- The ability to read and understand C code.
- Knowledge of common low-level vulnerabilities such as buffer overflows, format string vulnerabilities, etc.
- A general understanding of assembly instructions.
- An understanding of memory regions, specially within embedded systems.

## Setup

When we import the `.nds` file into Ghidra, the `Ndsware` Ghidra extension recognises it as an NDS ROM and selects the necessary language.

![Load Window](images/load-window.png)

Upon clicking "OK", the `Ndsware` loader, extracts the ARM9 code and overlay sections from the `.nds` file, and inserts them into memory at the correct base addresses. The loader also defines the other uninitialised regions of the memory map.

![Memory Map](images/memory-map.png)

Before running the auto analysis, we should decompile and mark the entry function at `0x2000800`. We should also rename the function as `entry`, so that the auto analysis identifies it as the entry.

## Identifying Standard (Nitro SDK) Functions

Before continuing, it's important to explain what we mean by standard functions in the context of Nintendo DS games. In typically C-based binaries, standard functions refer to functions that are implemented in `libc` such as `memset`, `memcpy`, `strcpy`, `strcmp`, `printf`, `puts`, `gets`, etc. However, Nitendo DS games instead use a custom set of standard functions defined in the [Nitro SDK](https://twlsdk.randommeaninglesscharacters.com/docs/nitro/NitroSDK/index.html). The Nitro SDK contains custom implementations of the many of these `libc` functions. For example, instead of `memset` and `memcpy`, the SDK contains [`MI_CpuFill`](https://twlsdk.randommeaninglesscharacters.com/docs/nitro/NitroSDK/mi/memory/MI_CpuFill.html) and [`MI_CpuCopy`](https://twlsdk.randommeaninglesscharacters.com/docs/nitro/NitroSDK/mi/memory/MI_CpuCopy.html). It also contains functions for handling 2D/3D graphics, interacting with the operating system, accessing game files stored on the ROM, and many other aspects of the Nintendo DS.

As discussed in the [challenges](#challenges) section, the binary doesn't include symbols, so we can't immediately see standard functions. Identifying these functions is vital because they provide valuable context on how data is being used in more complex functions. Therefore, it's important to identify as many standard functions as possible before reversing-engineering larger systems within the game. 

To identify standard memory functions (e.g., `MI_CpuCopy`), we're looking for function that appear to have very basic behaviour such as moving memory between variables and/or performing basic comparisons. Ideally, these functions should NOT call other functions or reference global variables/constants. A good way to find these standard functions is to pick a random function and follow the function call tree until we reach the end. Also, since these standard functions are essentially the basic building blocks of most other functions within the game, we would expect them to be called many times throughout the binary. Therefore, another good indicator is if the function has many references.

In the Nitro SDK, there is a set of ["STD" functions](https://twlsdk.randommeaninglesscharacters.com/docs/nitro/NitroSDK/std/list_std.html) for handling strings. Many of these functions appear to be custom implementations of the `str` functions in `libc`. For example, instead of `srcpy`, `strstr`, and `strcmp`, SDK has [`STD_CopyString`](`https://twlsdk.randommeaninglesscharacters.com/docs/nitro/NitroSDK/std/string/STD_CopyString.html), [`STD_SearchString`](https://twlsdk.randommeaninglesscharacters.com/docs/nitro/NitroSDK/std/string/STD_SearchString.html), and [`STD_CompareString`](https://twlsdk.randommeaninglesscharacters.com/docs/nitro/NitroSDK/std/string/STD_CompareString.html). The best way to find these functions is to look at the defined string in the binaries and search through the references. We're looking for function calls where a defined string is passed in as an argument.

Once we find one standard function, we should search for other functions in the same area memory because functions from the same library will appear next to each other. For example, when I found `STD_CompareNString` at `0x02089cd8`, I looked above it in the listing and found `STD_ConcatenateString` at `0x02089b44`.

Identifying standard functions can be very useful because we can use them workout the size of variables, structs, or struct fields. For example, in the function below there is a call to [MI_CpuClear](https://twlsdk.randommeaninglesscharacters.com/docs/nitro/NitroSDK/mi/memory/MI_CpuClear.html). `MI_CpuClear` takes 2 arguments: A `pointer` to some data, and the `size` of the data. It then sets all bytes in that data to zero. In this call to `MI_CpuClear`, the `size` parameter is 12, so we now know the size of `field_0x10` in `astruct_45` is 12 bytes.

```c
void FUN_0201b33c(astruct_45 *param_1)

{
    param_1->field64_0x40 = 0;
    FUN_0200b67c(&param_1->field_0x20);
    if (param_1->field28_0x1c == '\0') {
        return;
    }
    MI_CpuClear(&param_1->field_0x10,0xc);
    param_1->field28_0x1c = '\0';
    return;
}
```

These small clues scattered in different functions across the program can help us reconstruct definitions of structs. We can find all calls to `MI_CpuClear` and modified struct definitions as we go. This can be done for other similar functions like `MI_CpuFill` and `MI_CpuCopy`.
