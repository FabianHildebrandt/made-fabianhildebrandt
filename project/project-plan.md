# Project Plan

## Title
<!-- Give your project a short title. -->
**SCA 2024** - Sustainability Championship of America 2024

## Main Question

<!-- Think about one main question you want to answer based on the data. -->
1. Which countries are America's current sustainability champions, the rising stars and latecomers?

## Description

<!-- Describe your data science project in max. 200 words. Consider writing about why and how you attempt it. -->
### Brainstorming
- Three overall ratings: 1 overall champion, 1 rising star and 1 latecomer 
- Three categories: Environmental champion, Economic champion, Social champion
- 3-5 indicators per category (depending on data availability)
- Fair comparison: comparative metrics that don't penalise small & poor countries
- Possible comparison of indicators and their weights:
- energy mix, CO2 footprint, resource recycling, resource usage
- Overall champs: Solid performance across all categories
- Rising stars: Strong improvements in the last years
    - Show countries large growth rates for renewables in the energy mix, 
    - large decline rates in CO2 emissions
    - dropped resource consumption
    - increasing recycling rate
- Latecomers: Weak performance and low improvement rates
    - countries with the dirtiest electricity mix
    - countries with a high number of natural disasters
    - countries with the lowest recycling rates & trash production
- metadata for each country: North, middle, south america, number of inhabitants, location/ tag for map visualization

Environmental Indicators:
1. Carbon emissions
- **CO2 emissions per capita**
- Total greenhouse gas emissions

2. Energy
- **Renewable energy share in total energy mix**
- Access to clean energy

3. Natural Resources
- **Forest coverage and deforestation rates**
- Water stress levels
- Biodiversity indices
- **Waste management and recycling rates**

Social Indicators:
1. Health & Wellbeing
- **Life expectancy**
- Access to healthcare
- **Air quality indices**

2. Education
- Literacy rates
- Years of schooling
- **Access to education**

Economic Indicators:
- **Carbon intensity (emissions per GDP)**
- **Energy efficiency (energy use per GDP)**
- Green GDP
- Circular economy metrics
- Sustainable investment levels


## Datasources

<!-- Describe each datasources you plan to use in a section. Use the prefic "DatasourceX" where X is the id of the datasource. -->

### Datasource1: ExampleSource
* Metadata URL: https://mobilithek.info/offers/-6901989592576801458
* Data URL: https://raw.githubusercontent.com/od-ms/radverkehr-zaehlstellen/main/100035541/2019-01.csv
* Data Type: CSV

Short description of the DataSource.

## Work Packages

<!-- List of work packages ordered sequentially, each pointing to an issue with more details. -->
1. Setup a table of indicators [#1](https://github.com/FabianHildebrandt/made-fabianhildebrandt/issues/1)
2. Identifying suitable datasources [#2](https://github.com/FabianHildebrandt/made-fabianhildebrandt/issues/2)
3. Data inspection & verification of all datasources [#3](https://github.com/FabianHildebrandt/made-fabianhildebrandt/issues/3)
4. Creation of an automated data pipeline for the selected datasets [#4](https://github.com/FabianHildebrandt/made-fabianhildebrandt/issues/4)
5. Data Report [#5](https://github.com/FabianHildebrandt/made-fabianhildebrandt/issues/5)
6. Implement automated testing in the pipeline [#6](https://github.com/FabianHildebrandt/made-fabianhildebrandt/issues/6)
7. Continuous Integration [#7](https://github.com/FabianHildebrandt/made-fabianhildebrandt/issues/7)
8. Data analysis [#8](https://github.com/FabianHildebrandt/made-fabianhildebrandt/issues/8)
9. Project Report [#9](https://github.com/FabianHildebrandt/made-fabianhildebrandt/issues/9)
