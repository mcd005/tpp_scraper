# tpp_scraper

The 'tpp.py' program goes through the JSON files in the given fake hospital patients dataset and reorganises it into an easy to use dictionary of general details. It also sequences all the observations over time a patient has had, this would be difficult to generalise for patients with a different number of observations if inputting into a neural network. To combat this I chose to break this list into 3 features: average reading, gradient and range (these can easily be adapted depending on what the statitician would need).

The 'analysis.py' file guides you through how to build datasets, visualise and export to csv. 

# Instructions:
- Extract 'fhir.7z' into the diectory with the files tpp.py and analysis.py
- From terminal run 'python tpp.py', this extracts all the features specified in the file into a more useable format (described above).
- Perform analysis:
  - Run 'python analysis.py', this walks you through how to use the interface.

The analysis file can visualise and create datasets and then export the dataset when you're done into csv format
