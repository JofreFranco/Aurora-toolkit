# Aurora

This collection of codes helps to automate the analysis of multiple sine sweep measurements when using Aurora Acoustical Parameters with Audacity.

Since the convolution of Aurora in Audacity does not work properly when appying it to multiple files and room measurements usually have several audios, the convolver.py code automatically convolves several files in a folder with a inverse filter and save the room impulse responses obtained. The measurement_separator.py separates a single audio containing all measurements of the room. Preproc.py integrates both processes.

AuroraText.py reads the CSV file given by Aurora Acoustical Parameters into a Pandas DataFrame so it is eassier to analyze, process, plot and understand.
