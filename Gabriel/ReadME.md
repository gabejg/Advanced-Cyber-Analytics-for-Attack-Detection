All documents, present in either the main folder as such or in corresponding subfolders contribute towards the 'Advanced Cyber Analytics for Anomaly Detection' project and are exclusively the work of named contributor and his project colleagues. All extra material is adequately referenced and documented within these documents, wherever relevant. 

The files can be understood as independent works for the most part, but they are grouped based on the stages of the project they were used in. All files are meant to be read in the order indicated numerically within their folders, e.g. 1 - X, 2 - Y etc. The chronological (and advised) reading order for the folders is as follows:


## 00. Folder: 'Notes and Settings' [OPTIONAL]

This folder is where I have stored references, used packages and other small test pieces of code that do not fit anywhere else in the repository. It is purely there for tracking purposes and as a store for unused code that could be useful to refer to.
    
## 01. Folder: 'NetFlow'

This subfolder is dedicated to the start of the project attempts at deciding between the two types of datasets provided by Los Alamos National Laboratory: The 'ATI dataset' consisting of Authentications and Processes that the team ended up working on, or the 'Netflow dataset' consisting of ~ 1TB of unfiltered traffic over the course of 90 days. The folder addresses all the issues that rose in this process and why we therefore decided to work with the ATI dataset instead.
    

[## 02. Folder: 'EDA']()

This subfolder marks the first relevant contact with the dataset we worked with - where we conducted Exploratory Data Analysis. It contains elements such as: data cleaning, visual analysis on the Authentications, graphing and networking techniques.
    
## 03. Folder: 'Plots'

This is a seperate folder heavily linked to 02 - EDA, as a central store for easier access and indexing of plots I made during this stage - as well as during additional stages of the project.

## 04. Folder: 'Anomaly Detection'

This folder consists of work done during the Anomaly Detection part of our project, for my part this mostly involved testing of others code in various ways to try and achieve better results, as well as a relatively in depth look at reducing the data to increase the efficiency of our algorithms.