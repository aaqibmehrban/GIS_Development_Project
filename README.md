# GIS Development Project

## Project Requirements
Your organization has been hired by the City of Helsinki to do an urban climate analysis for the Helsinki city centre development plan. However, before the actual analysis work can be started, you need to figure out the best way to approach the problem. Thus, you have been given the task of figuring out how to tackle the challenge.

Helsinki City is interested in how blue and green infrastructure behave at street level and how they could lead to improving the urban climate and thermal comfort along with creation of lively centres for people to get together and spend pleasant and quality time there. The pedestrian, sitting and cycling areas in Helsinki city centre will be expanded in early summer 2026. The climate responsive proposal is expected to be inclusive and provide fair opportunities for all.

In 2023, Helsinki City planned to have temporary pedestrian and cycling areas on Esplanadi streets, Kasarmikatu, Erottajankatu, Korkeavuorenkatu in front of the Design Museum and on Lönnrotinkatu. Due to the positive impacts of such temporary interventions for a lively and comfortable city centre with flourishing brick-and-mortar shops, pleasant sitting and meeting places, the council is looking for a permanent solution to make the outdoor experience, pleasant and lively for its users in terms of utilising urban greenery and blue infrastructure.

The Urban Multi-scale Environmental Predictor (UMEP) is a climate service tool, designed for researchers and service providers (e.g. architects, climatologists, energy, health and urban planners) presented as a plugin for QGIS. This tool can also be used for processing without accessing QGIS graphical user interface. The tool can be used for a variety of applications related to outdoor thermal comfort, urban energy consumption, climate change mitigation etc.

In this work, your task is to see what open geospatial data can be used as source data for the calculation and to create a prototype web application for urban climate modeling data. In the prototype, only publicly available data will be used as input. Therefore, the possible regulations and planning guides for such permanent change and how they can be taken into account will need some adjustment for this prototype service. If possible, the client would like you to also investigate the suitability of Helsinki 3d datasets as input data for the analysis. The client is aware that the results of this project will be a best-effort solution instead of a full implementation of a microclimate simulation.

## Data

  1. Digital Elevation Data - NLS: https://asiointi.maanmittauslaitos.fi/karttapaikka/tiedostopalvelu
  2. Wind Map Data - https://globalwindatlas.info/en
  3. Canopy data - HSY: https://kartta.hsy.fi/
  4. Building data for DSM: QGIS: QuickOSM-plugin

## Installation and Run

  1. Install Python 3.9 or above
  2. Then install modules using 'pip3 install -r requirements.txt'
  3. Install Geoserver and upload kayers data too it.
  4. Run app.py file to start web.
