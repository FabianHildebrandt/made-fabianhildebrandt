# Project Plan

## Title
<!-- Give your project a short title. -->
**SCA 2024** - Sustainability Championship of America 2024

## Main Question

<!-- Think about one main question you want to answer based on the data. -->
**Which countries are America's current sustainability champions, the rising stars and latecomers?**

## Description

<!-- Describe your data science project in max. 200 words. Consider writing about why and how you attempt it. -->
- Three  ratings: 1 overall champion, 1 rising star and 1 latecomer 
- Three categories: Environmental champion, Economic champion, Social champion
- 2-5 indicators per category (depending on data availability)
- Fair comparison: all indicators are handpicked comparative metrics that don't penalise small & poor countries
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
- The indicators are subject to **change**. The indicators are evaluated based on their data quality (year and country coverage etc.). The goal is to have current indicators, which are not outdated. The pipeline is configurable and generic. Indicators can be removed and added without big effort.

| Name                                      | Weight | Data Source ID | Possible Reliable Data Sources                  |
|-------------------------------------------|--------|----------------|------------------------------------------------|
| **Environmental Indicators**              | 0.5 |
| (1) Emissions per capita                  ||[DS01](#ds01-world-bank-group) | IPCC, World Bank, National Statistics Offices   |
| (2) Renewable energy share ||[DS01](#ds01-world-bank-group) | IEA, REN21, World Bank                         |
| (3) Deforestation rates/ emissions   ||[DS01](#ds01-world-bank-group)| FAO, Global Forest Watch, National Forestry Agencies |
| (4) Water stress levels                       || [DS01](#ds01-world-bank-group)| WRI Aqueduct, FAO, UNEP                        |
| (5) Waste equivalent emissions      || [DS01](#ds01-world-bank-group) | OECD, Eurostat, World Bank                     |
| **Social Indicators**                     | 0.3 |
| (6) Health expenditure             ||[DS01](#ds01-world-bank-group)| WHO, UN Population Division |
| (7) Air pollution                       || [DS01](#ds01-world-bank-group) | WHO, AQI Databases, National Environmental Agencies |
| (8) Education efficiency                       || [DS01](#ds01-world-bank-group)| UNESCO, UNICEF, World Bank                     |
| **Economic Indicators**                   |0.2 |
| (9) Carbon intensity (emissions per GDP)      ||[DS01](#ds01-world-bank-group) | IPCC, IEA, National Statistics Offices         |
| (10) Research and development expenditure    || [DS01](#ds01-world-bank-group) | IEA, World Bank, UNIDO                         |



## Datasources

<!-- Describe each datasources you plan to use in a section. Use the prefic "DatasourceX" where X is the id of the datasource. -->

### DS01: WORLD BANK GROUP
* Metadata URL: automatically created for each selected series
* Data URL: https://databank.worldbank.org/source/world-development-indicators/
* Data Type: XLSX, CSV, Tabbed TXT, Pandas DataFrame

The WORLD BANK GROUP offers a really comprehensive composed dataset called *World Development Indicators* containing most of the listed indicators.The database of the WORLD BANK is composed of numerous publications, statistics and evaluations. It provides a flexible user interface to select the countries, indicators (series), time range and a comprehensive list of metadata attributes. After completing the selection, the data can be downloaded (CSV, XLSX, Tabbed TXT). The data is usually availably under the CC BY-4.X license. Additionally, it offers an open API, which can be accessed using the open source library [wbgapi](https://pypi.org/project/wbgapi/) under the MIT License.
An FAQ contains more information regarding [licensing](https://datacatalog.worldbank.org/public-licenses#cc-by) of the indicator data.


**List of indicators**
1. Carbon dioxide (CO2) emissions excluding LULUCF per capita (t CO2e/capita) - EN.GHG.CO2.PC.CE.AR5 / Total greenhouse gas emissions excluding LULUCF per capita (t CO2e/capita) - EN.GHG.ALL.PC.CE.AR5
2. Renewable energy consumption (% of total final energy consumption) - EG.FEC.RNEW.ZS
3. Carbon dioxide (CO2) net fluxes from LULUCF - Deforestation (Mt CO2e) - EN.GHG.CO2.LU.DF.MT.CE.AR5
4. Level of water stress: freshwater withdrawal as a proportion of available freshwater resources - ER.H2O.FWST.ZS
5. Carbon dioxide (CO2) emissions from Waste (Mt CO2e) - EN.GHG.CO2.WA.MT.CE.AR5
6. Current health expenditure (% of GDP) - SH.XPD.CHEX.GD.ZS / Current health expenditure per capita (current US$) - SH.XPD.CHEX.PC.CD
7. Mortality rate attributed to household and ambient air pollution, age-standardized (per 100,000 population) - SH.STA.AIRP.P5 / PM2.5 air pollution, population exposed to levels exceeding WHO guideline value (% of total) - EN.ATM.PM25.MC.ZS
8. Literacy rate, adult total (% of people ages 15 and above) - SE.ADT.LITR.ZS
9. Carbon intensity of GDP (kg CO2e per 2021 PPP) - EN.GHG.CO2.RT.GDP.PP.KD , Carbon intensity of GDP (kg CO2e per constant 2015 US$ of GDP) - EN.GHG.CO2.RT.GDP.KD
10. Research and development expenditure (% of GDP) - GB.XPD.RSDV.GD.ZS

### DS02: tbd
* Metadata URL: 
* Data URL: 
* Data Type: 

List of indicators
1.
2.
3.
4.
5.
6.
7.
8.
9.
10.

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
