![Image of CompareML](https://raw.githubusercontent.com/i3uex/CompareML/master/public/img/CompareMLheader.png)

# [CompareML](http://167.172.177.191:8080/)

#### Welcome to the *CompareML* Developer Manual

[![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](https://github.com/i3uex/CompareML/blob/master/LICENSE)

Notas: 
- Meter sección de deployment describiendo como desplegar esta aplicación
- Meter hiperparámetros de los algoritmos
- Completar sección outputs con regresión



## Table of Contents
- [1. *CompareML* Overview](#1-compareml-overview)
- [2. *CompareML* Architecture](#2-compareml-architecture)
    - [2.1. Front-End User Interface](#21-front-end-user-interface)
    - [2.2. Back-End main Application](#21-back-end-main-application)
    - [2.3. Back-End Split Function](#21-back-end-split-function) 
    - [2.4. Providers Modules](#24-providers-modules)
- [3. List of Machine Learning libraries and services supported](#3-list-of-machine-learning-libraries-and-services-supported)
    - [3.1. Turi Graphlab Create](#31-turi-graphlab-create)
    - [3.2. Scikit Learn](#32-scikit-learn)
    - [3.3. R](#33-r)  
- [4. List of Machine Learning algorithms supported](#4-list-of-machine-learning-algorithms-supported)
    - [4.1. Regression Algorithms](#41-regression-algorithms)
        - [4.1.1. XXX](#411-xxx)
        - [4.1.2. XXX](#412-xxx)
        - [4.1.3. XXX](#413-xxx)
     - [4.2. Classification Algorithms](#42-classification-algorithms)
        - [4.2.1. Decision Forest](#421-decision-forest)
        - [4.2.2. XXX](#422-xxx)
        - [4.2.3. XXX](#423-xxx)
- [5. *CompareML* Business Process](#5-compareml-business-process)  
- [6. *CompareML* File Structure](#6-compareml-file-structure)
- [7. Functionalities](#7-functionalities)
- [8. Inputs](#8-inputs)
- [9. Outputs](#9-outputs)
- [10. Deployment](#10-deployment)



## 1. *CompareML* Overview

*CompareML* is a comparator for machine learning algorithms libraries and services. It makes it easy for users to create a test model of their dataset in three of the most widespread options such as Scikit-Learn, Turi Graphlab and R libraries and, at the same time, allows selecting different well-known classification and regression algorithms available in all providers. 

The characteristics of *CompareML* facilitates data scientists the task of choosing the most suitable provider for their data, improving notably the experiment results while reducing time and costs. Furthermore, *CompareML* helps them in selecting the algorithms which are liable to produce the best results for their datasets.  

## 2. *CompareML* Architecture

[comment]: <Although *CompareML* has been implemented following a classical  MVC (model-view-controller) software architecture, the architecture has been designed following the concepts of a hybrid microservice-based architecture. The microservices architecture improves fault toleration through the isolation of certain modules which are designed with different technologies and/or libraries, facilitates continuous integration (CI) and continuous delivery (CD) that allows us to produce software in short cycles during the evolution of the different functionalities of each module and facilitates understanding the functionality.> 

*CompareML* has been implemented following a classical Client Server software architecture with a MWC (model view controller) approach. The server hosts the resources that manage the creation of models and deliver the results to the client. The client interacts with end-users through its user interface and initiate request to the server. This architecture is graphically illustrated in the following figure: 

[comment]: <It has not been considered, at least at this version, a pure microservice-based architecture approach following strict requirements in order to not overload with communication messages the whole infrastructure to optimize resources. As a result, it is recommended a hybrid microservice-based inspire architecture, which is graphically illustrated in the following figure. >

![CompareML Architecture](https://raw.githubusercontent.com/i3uex/CompareML/master/public/img/softwareArchitecture.png)

In the following subsections the *CompareML* modules are described.

### 2.1 Client

It deals with the presentation layer and it is in charge of interacting with users. In this module, users upload the dataset and set the configuration of the experiments that are sent to the server-side. When the experiments are carried out, the results are sent back to this module to be shown to users in a friendly manner. 

The user interface has been designed to maximize usability being simple, consistent and offering cross-browser compatibility. This module has been developed using widespread technologies such as HTML5, CSS3, and JavaScript. 

### 2.2 Back-End main Application

The Back-End main application is the core of *CompareML*. It is in charge of coordinating and controlling the software operational processes. The Back-end receives the conditions under which the experiments must be carried out from the User Interface and call the web services of the Turi Graphlab Create, Scikit-Learn and R modules required, sending them the conditions of the experiments that affect them (algorithms selection, training dataset, test dataset, ...). When the execution of the modules is finished, it receives the results and send them back to the user interface. This module has been developed using Python. 

### 2.3 Back-End Split Function

The split function is a special module in the back-end that deal with the problem of splitting the dataset uploaded by the end-user and received from the user interface into two subsets: the training dataset containing the 80% of the instances of the total dataset and the test dataset containing the other remaining 20% of the instances. This task is carried out in this module because it is necessary to ensure that the experiment results are as objective as possible. If each module that conducts the experiment (Scikit Learn, Turi Graphlab and R) divides the dataset itself randomly, the random seed would be different and this has potentially negative implications in the objective comparison of the models created through each module. This module has been developed using Python and Pandas, a powerful open source data analysis and manipulation tool, built on top of the Python programming language. 


### 2.4 Providers Modules

This module contains the implementations of the classification Decision Forest, XXX algorithms and the regression XXX algorithms using Scikit Learn. It makes use of the *sklearn* library to build and evaluate the models and the *pandas* library to manipulate data using its *DataFrame* data structure and functions. These modules receive as inputs the algorithms that need to be used to build models, the providers, and the training and evaluation datasets. When the experiments are carried out, the results are sent back to the Back-end main application module.

The functionalities of the machine learning providers, i.e., the experiments carried out using each provider's libraries, data structures and functions are isolated within the server-side to facilitate its development.

   
    
##  3. List of Machine Learning libraries and services supported

*CompareML* version 1 support the following machine learning libraries and services ready to be isolated each one of them in a module of the pool of microservices:

### 3.1 Turi Graphlab Create

This module contains the implementations of the classification Decision Forest, XXX algorithms and the regression XXX algorithms using Turi Graphlab Create. It makes use of the *turicreate* library to build and evaluate the models and the *pandas* and *Sframe* libraries to manipulate data using its *DataFrame* and *Sframe* data structure and functions respectively. 

GraphLab Create is a Python package that allows programmers to perform end-to-end large-scale data analysis and data product development. It is a distributed computation framework written in C++ developed at the Carnegie Mellon University acquired by Apple Inc. in 2016.


### 3.2. Scikit Learn

This module contains the implementations of the classification Decision Forest, XXX algorithms and the regression XXX algorithms using Scikit Learn. It makes use of the *sklearn* library to build and evaluate the models and the *pandas* library to manipulate data using its *DataFrame* data structure and functions. 

Scikit-Learn is one of the most popular machine learning libraries. It is largely written in Python with some core algorithms written in Cython to improve performance. It is supported by several institutional and private grants. 


### 3.3 R

This module contains the implementations of the classification Decision Forest, XXX algorithms and the regression XXX algorithms using R. It needs to be emphasised that the R code is running embedded in Python, through the access provided by the *rpy2* library. 

It makes use of the \textit{xxx} library to xxxxx}. 

## 4. List of Machine Learning algorithms supported

### 4.1 Regression Algorithms

#### 4.1.1 XXX

#### 4.1.2 XXX

#### 4.1.3 XXX

### 4.2 Classification Algorithms

#### 4.2.1 Decision Trees

Decision trees algorithms build a tree-like structure where each node represents a question over an attribute. The answers to that question create new branches to expand the structure until the end of the tree is reached, being the leaf node the one that indicates the predicted class. The *Decision Forest* (DF) algorithm is an improvement that creates several decision trees, using bagging or other technique, and votes the most popular output of them. Usually, most of the implementation does not directly count the output of them but sum the normalized frequency of each output in each tree to get the label with more probability. 

#### 4.2.2 XXX

#### 4.2.3 XXX



## 5. *CompareML* Business Process

In order to further show the *CompareML* logic and to better illustrate the module relationships and their business process, a BPMN (Business Process Model and Notation) diagram has been created. In this diagram, shown below, the relations between the client-side and the server-side (included the providers' modules) can be tracked easily.

![BPMN Diagram](https://raw.githubusercontent.com/i3uex/CompareML/master/public/img/bpmn_diagram_horizontal.png)


## 6. *CompareML* File Structure

The *CompareML* file structure is graphically illustrated in the following figure: 

![CompareML FileStructure](https://raw.githubusercontent.com/i3uex/CompareML/master/public/img/fileArchitecture.png)

The files of the client-side are index.html, style.css and client.js. They contain the HTML, CSS and JavaScript source code that build the graphical user interface and communicates with the server-side. 

The server-side contain the following files:

- main.py. It is in charge of turn of the *CompareML* service with the "python3 main.py &" command. It contains the web server configuration, defines the resources shown, and links with WebServer.py. It is implemented following the CherryPy framework.

- WebServer.py. It receives the input from the client-side and process it to be handled subsequently. The POST methods of the classes receive as parameters the information sent from the front-end (client). Notice that the name of the parameters must match the name of the variables sent from the front. The next pictures show an example:

![WebServerCapture0](https://raw.githubusercontent.com/i3uex/CompareML/master/public/img/wecapture0.png.png)
![WebServerCapture1](https://raw.githubusercontent.com/i3uex/CompareML/master/public/img/wscapture1.png.png)





- engine.py.
- turiGraphlab.py
- scikitLearn.py
- R.py



## 7. Functionalities

The list of functionalities can be found in the User Manual

[User Manual CompareML 1.0](https://raw.githubusercontent.com/i3uex/CompareML/master/CompareML%20User%20Manual.pdf)


## 8. Inputs

The inputs of *CompareML* version 1.0 are:

| Input Name    | Description   | Notes |
| ------------- |---------------| ------|
| Dataset       | The dataset must be in CSV format using a comma to separate values and it must contain a header row. | Notice that due that the comma is used as a separator, *CompareML* may not handle field data containing commas or embedded line breaks. Additionally, it may not handle other unconventional characters. |
| Label         | Feature that models will predict.   | After uploading a dataset, the label dropdown menu will load every existing feature in the dataset.  Users must select the label from the dropdown menu.   |
| Providers     | Machine Learning libraries and services available to build models   | The user must select at least one of them. *CompareML* version 1.0 supports Turi Graphlab Create, Scikit Learn and R. |
| Algorithms     | Regression and Classification algorithms available to build models.   | The user must select at least one of them. *CompareML* allow users to choose between the XXX, XXX, and XXX Regression algorithms and the Decision Forest, XXX, XXX Classification algorithms. |

Notice that, in version 1.0, *CompareML* does not automatically recognize the data type of the selected label so the experiments will be run regardless of the appropriateness of the label data type and the type of algorithms selected. In such cases, the results of the experiments will be given according to how each one of the libraries, services, and tools selected responds to these kinds of situations.



## 9. Outputs

The outputs of *CompareML* version 1.0 are a set of metrics that allow studying the convenience of the models created using different algorithms from different machine learning tools and services. They vary depending on the user's algorithms selection.

If the user select Regression algorithms the outputs are:

| Output Name   | Description   | 
| ------------- |---------------| 
| xxx       | The dataset must be

If the user select Classification algorithms the outputs are:

| Output Name   | Description   | 
| ------------- |---------------| 
| Matrix Confusion      | Table layout where each row represents the number of instances of each class and each column represents the class that has been predicted by the model. A confusion matrix is created for each algorithm selected. |
| Accuracy              | It indicates the correctly predicted instances (number of correctly predicted items / total of items to predict). An accuracy value is given for each algorithm selected. |
| Precision             | It indicates the proportion of predicted positives. With the confusion Matrix it can be calculated as: (number of true positives / (number of true positives + number of false positives). A precision value is given for each algorithm selected.|
| Recall (Sensitivity)  | It indicates the proportion of proportion of positives predicted as positives. With the confusion Matrix it can be calculated as: (number of true positives / (number of true positives + number of false negatives). A recall value is given for each algorithm selected. |


## 10. Deployment

How to deploy the project --esta parte la puede redactar Andy--

En Linux:
➔	apt-get install r-base
➔	pip3 install cherrypy
➔	pip3 install turicreate
➔	pip3 install scikit-learn
➔	pip3 install tzlocal
➔	pip3 install rpy2

En R:
➔	install.packages("randomForest")
➔	install.packages("caret", dependencies = T)
➔	install.packages("e1071")



