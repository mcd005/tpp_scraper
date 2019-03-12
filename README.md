# tpp_scraper

This program goes through the JSON files in the given fake hospital patients dataset and reorganises it into an easy to use dictionary of general details. It also sequences all the observations over time a patient has had, this would be difficult to generalise for patients with a different number of observations if inputting into a neural network. To combat this I chose to break this list into 3 features: average reading, gradient and range (these can easily be adapted depending on what the statitician would need).
