<p align="center">

  <a href="https://imgur.com/U3PUiCS"><img src="https://i.imgur.com/U3PUiCS.png" title="source: imgur.com" /></a>


  <h3 align="center"></h3>

</p>


## Table of contents

- [Introduction](#introduction)
- [What's included](#whats-included)
- [Creators](#creators)
- [Thanks](#thanks)
- [Copyright and license](#copyright-and-license)


## Introduction

This repo contains the code I made for my master's thesis. The purpose of this project is control the batteries charge cycle of a house in a smart way in order to save energy and reduce the needed capacity of the batteries. Besides, increasing the charging-decision frequency can lead to better battery life expectancy as the batteries are less exposed to full charging cyles.

Using big data and deep learning tools, it is possible to forecast electric consumption and compare the result to the power output from a solar panel array. The comparision will determine the behaviour of the charging profile of the batteries.

The whole project can be reached at www.sampletext.com


## What's included

This is the folder structure. All source code is under src folder. There's a test script that can be used to verify the functionality. Results are stored in csv format at /Data/charge_battery_data.csv.

Data analysis and model building are under /JupyterNotebooks.

```text
TFM-git/
└── /
    ├── Data/
    │   ├── consumos_model.h5
    │   └── scaler.pkl
    ├── JupyterNotebooks/
    │   ├── build_model.ipynb
    │   └── battery_and_solar_panels.ipynb
    └── src/
        ├── smart_algorithym.py
        ├── bateria.py
        ├── main.py
        ├── test.py
        └── functions.py
        
```


## Creators

**Ricardo Gomez**

- [LinkedIn](https://www.linkedin.com/in/ricardogomez-al)

## Thanks

Special thanks to my tutors for suggesting the idea!  
- Raúl Gonzalez Medina  
- Emilio Figueres Amoros  

## Copyright and license

Code released under the [MIT License](https://reponame/blob/master/LICENSE).

