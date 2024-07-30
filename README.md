# sqldumptojson: A Converter
This performant tool converts a mysqldump file to a JSON representation of a table to make it easy to import a SQL dump into Elastic indexes.

![license](https://img.shields.io/github/license/MartinPaulEve/sqldumptojson) ![activity](https://img.shields.io/github/last-commit/MartinPaulEve/sqldumptojson)
 
## Installation
Although this is a Python application, it uses a Rust library. You may need to [install rustup](https://www.rust-lang.org/tools/install). 
    
        pip install -r ./requirements.txt

## Usage

     Usage: sqldumptojson.py [OPTIONS] FILE TABLE [OUTPUT_DIRECTORY]                                                                                                                                                                        
                                                                                                                                                                                                                                            
     Convert a SQL dump to JSON files                                                                                                                                                                                                       
                                                                                                                                                                                                                                            
    ╭─ Arguments ────────────────────────────────────────────────────────────────────────────────────────────────╮
    │ *    file                  TEXT                The input SQL dump file to parse [default: None] [required] │
    │ *    table                 TEXT                The SQL table file to recreate [default: None] [required]   │
    │      output_directory      [OUTPUT_DIRECTORY]  The output directory for the JSON files [default: output]   │
    ╰────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

&copy; Martin Paul Eve 2024
