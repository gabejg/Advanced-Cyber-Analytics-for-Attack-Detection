All documents, present in either the main folder as such or in corresponding subfolders contribute towards the 'Advanced Cyber Analytics for Anomaly Detection' project and are exclusively the work of named contributor and his project colleagues. All extra material is adequately referenced and documented within these documents, wherever relevant. 

The files can be understood as independent works for the most part, but they are grouped based on the stages of the project they were used in. All files are meant to be read in the order indicated numerically within their folders, e.g. 1 - X, 2 - Y etc. The chronological (and advised) reading order for the folders is as follows:


0. Folder: 'Early Project Works' [OPTIONAL]

    This subfolder has been left in mostly for record keeping. It contains NO FILES THAT WERE LATER DIRECTLY USED TOWARDS THE PROJECT. However, it does contain methods, algorithms, structures or other types of investigations that were deemed relevant enough towards the project itself to be kept. Particularly, the 'WaterTreatment' files reference a very early dataset that was proposed as the main source of investigation for the project. Likewise, 'Alerts.csv' contains another such dataset, one that was considered a bit later in the stages of project preparation for its notable affiliation to papers investigating Kill-Chain linkage to cyberattacks. There is no advised reading order for this folder.
    

1. Folder: 'NetFlow'

    This subfolder is dedicated to the start of the project attempts at deciding between the two types of datasets provided by Los Alamos National Laboratory: The 'ATI dataset' consisting of Authentications and Processes that the team ended up working on, or the 'Netflow dataset' consisting of ~ 1TB of unfiltered traffic over the course of 90 days. The folder addresses all the issues that rose in this process and why we therefore decided to work with the ATI dataset instead.
    

2. Folder: 'Exploratory Data Analysis'

    This subfolder marks the first relevant contact with the dataset we worked with. It contains elements such as: data cleaning, visual analysis on the Authentications, graphing and networking techniques, analysis of the initial results and links to the next stage of the project. This folder is crucial for further reference, as results drawn from the initial steps described within the corresponding files are later cited in the third and fourth folders. 
    

3. Folder: 'Anomaly Detection'

    This subfolder contains all my contribution towards performing the anomaly detection stage of the project. This task was mainly distributed among two other contributors, and hence the core of our team's anomaly scores and, detection attempts as well as the final set of anomalies identified can be found in their respective folders, and in the common 'Data' folder respectively. However, files from this subfolder have been used in the initial stages of anomaly detection, as well as towards the verification and validation of final results. The 'Comparing usernames' file contains an analysis done prior to any model or technique implementation, which then helped structure an anomaly detection method. Similarly, the 'Decision tree' was then used for estimating the FPR-rates of our results. 


4. Folder: 'Kill Chain'

    This subfolder contains my contribution towards the most substantial and novel results of our inquiry. I, along with a colleague, were mainly tasked with researching, defining, devising the model for and implementing the Kill Chain (while our colleagues were working on anomaly detection techniques). Therefore, this folder contains most of the work done towards the final set goal of the project: classifying anomalies into Kill Chain stages. The files represent, in consecutive order, the work done towards achieving that goal. The stages of the Kill Chain our team has established working with can be found in the 'Kill Chain research' file.