# CISC689: Natural Language Processing Homework 3  
Author: Carlton Brady (solo)  
Python version: 3.6.3  
dependencies:  
nltk  

**Files**  
Folder: trained_models  
    a_chunker = pickle file containing the trained model from Q1 part a  
    b_chunker = pickel file containing the trained model from Q1 part b  
    c_chunker = pickle file containing the trained model from Q1 part c  
  
Folder: results  
    a_chunker_results.txt = results from running chunker from part a on the HW3_test.txt sentences  
    b_chunker_results.txt = results from running chunker from part b on the HW3_test.txt sentences  
    c_chunker_results.txt = results from running chunker from part c on the HW3_test.txt sentences  
    charlie_chaplin_results.txt = data entities extracted from charlie chaplin wiki page  
    constitution_of_the_united_states_results.txt = data entities extracted from US constitution wiki page  
    daylight_saving_time_results.txt = data entities extracted from daylight saving time wiki page  
    nobel_prize_results.txt = data entities extracted from nobel prize wiki page  
    world_world_i_results.txt = date entities extracted from WWI wiki page  
    ner_results.txt = results from running ntlk.ne_chunk on the HW3_test.txt sentences  
  
Folder: wiki_pages:  
    charlie_chaplin.txt = wikipedia source file for charlie chaplin  
    constitution_of_the_united_states.txt = wikipedia source file for US constitution  
    daylight_saving_time.txt = wikipedia source file for daylight saving time  
    nobel_prize.txt = wikipedia source file for the nobel prize  
    world_world_i.txt = wikipedia source file for WWI  
  
HW3_test.txt = the given sentences to run the chunkers on  
chunking.py = script that loads the trained chunking models, runs them on the HW3_test.txt sentences, and writes the results to the chunking results files  
named_entity_recognition.py = script that runs nltk.ne_chunk on the HW3_test.txt sentences and writes the results to the ner_results.txt file  
date_entity_recognition.py = script that extracts date entities from the wikipedia source files and writes the results to the appropriate results files  
  
  
**How to run the code**  
The scripts can be run on the command line as follows:  
python3 chunking.py  
python3 named_entity_recognition.py  
python3 date_entity_recognition.py  
  
  
**Chunker for part a:**  
ChunkParse score:  
    IOB Accuracy:  92.9%%  
    Precision:     79.9%%  
    Recall:        86.8%%  
    F-Measure:     83.2%%  
   
**Chunker for part b:**  
ChunkParse score:  
    IOB Accuracy:  94.6%%  
    Precision:     84.6%%  
    Recall:        89.8%%  
    F-Measure:     87.1%%  
  
**Chunker for part c:**  
ChunkParse score:  
    IOB Accuracy:  95.5%%  
    Precision:     86.5%%  
    Recall:        90.3%%  
    F-Measure:     88.4%%  

