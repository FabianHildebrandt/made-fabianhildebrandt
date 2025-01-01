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
- sources for indicators: [Sovereign ESG Data Framework](https://esgdata.worldbank.org/data/framework?lang=en)

| Name                                      | Data Source ID | Possible Reliable Data Sources                  |
|-------------------------------------------|----------------|------------------------------------------------|
| **Environmental Indicators**              |
| (1) Emissions per capita                  |[DS01](#ds01-world-bank-group), [DS02](#ds02-data-on-co2-and-greenhouse-gas-emissions-by-our-world-in-data) | IPCC, World Bank, National Statistics Offices   |
| (2) Renewable energy share |[DS01](#ds01-world-bank-group), [DS02](#ds02-data-on-co2-and-greenhouse-gas-emissions-by-our-world-in-data) | IEA, REN21, World Bank                         |
| (3) Deforestation rates/ emissions   |[DS01](#ds01-world-bank-group), [DS02](#ds02-data-on-co2-and-greenhouse-gas-emissions-by-our-world-in-data)| FAO, Global Forest Watch, National Forestry Agencies |
| (4) Water stress levels                       | [DS01](#ds01-world-bank-group)| WRI Aqueduct, FAO, UNEP                        |
| (5) Waste equivalent emissions      | [DS01](#ds01-world-bank-group) | OECD, Eurostat, World Bank                     |
| **Social Indicators**                     |
| (6) Health expenditure             |[DS01](#ds01-world-bank-group)| WHO, UN Population Division |
| (7) Air pollution                       | [DS01](#ds01-world-bank-group), [DS02](#ds02-data-on-co2-and-greenhouse-gas-emissions-by-our-world-in-data) | WHO, AQI Databases, National Environmental Agencies |
| (8) Education efficiency                       | [DS01](#ds01-world-bank-group)| UNESCO, UNICEF, World Bank                     |
| **Economic Indicators**                   |
| (9) Carbon intensity (emissions per GDP)      |[DS01](#ds01-world-bank-group), [DS02](#ds02-data-on-co2-and-greenhouse-gas-emissions-by-our-world-in-data) | IPCC, IEA, National Statistics Offices         |
| (10) Green tech, Investments, R&D    | [DS01](#ds01-world-bank-group) | IEA, World Bank, UNIDO                         |
| (11) Climate Risk, Droughts, Floods, extreme temperatures  |[DS01](#ds01-world-bank-group) | |
| (12) Natural Resource Depletion    | [DS01](#ds01-world-bank-group) | |

### How to calculate the latecomers ranking
- for the latecomers ranking, the position in the rising star and overall ranking are averaged and then set into comparison with the climate risks / costs
- high costs/ a high risk for droughts, floods etc. should result in a large urge for stricter sustainbality targets
- A low average Rising Star & Overall Ranking indicates (e. 1st, 2nd, 3rd) very good performance and a high ranking indicates bad performance (43rd, 42nd, 41st)
- Climate Costs: High ranking = High risks (43rd, 42nd, 41st), Low ranking = Low risks (1st, 2nd, 3rd)
- Challenge: The indicators for climate risks are barely reported or are only reported for the whole world -> 
that's why, it's hard to implement a comparative metric in that domain
- second idea: depletion of natural resources (how many percent of the country's resources have been used up)
- Natural resource depletion is the sum of net forest depletion, energy depletion, and mineral depletion. -> creates a comprehensive image


**List of indicators for the latecomers ranking**
 

1. Normalize the overall, rising stars and latecomers ranking (max normalization) to get a ranking from 0 to 1
2. Calculate a weighted average of the rankings (alpha as the weighting factor)
    - alpha determines how important the climate cost ranking is
3. Create a ranking from the scores

## Datasources

<!-- Describe each datasources you plan to use in a section. Use the prefic "DatasourceX" where X is the id of the datasource. -->

### DS01: WORLD BANK GROUP
* Metadata URL: automatically created for each selected series
* Data URL: https://databank.worldbank.org/source/world-development-indicators/
* Data Type: XLSX, CSV, Tabbed TXT, Pandas DataFrame

The WORLD BANK GROUP offers a really comprehensive composed dataset called *World Development Indicators* containing most of the listed indicators.The database of the WORLD BANK is composed of numerous publications, statistics and evaluations. It provides a flexible user interface to select the countries, indicators (series), time range and a comprehensive list of metadata attributes. After completing the selection, the data can be downloaded (CSV, XLSX, Tabbed TXT). The data is usually availably under the CC BY-4.X license. Additionally, it offers an open API, which can be accessed using the open source library [wbgapi](https://pypi.org/project/wbgapi/) under the MIT License.
An FAQ contains more information regarding [licensing](https://datacatalog.worldbank.org/public-licenses#cc-by) of the indicator data.


**List of indicators**
1. Emissions per capita:
    - Carbon dioxide (CO2) emissions excluding LULUCF per capita (t CO2e/capita) - EN.GHG.CO2.PC.CE.AR5
    - **Total greenhouse gas emissions excluding LULUCF per capita (t CO2e/capita) - EN.GHG.ALL.PC.CE.AR5**
2. Renewable energy share:
    - **Renewable energy consumption (% of total final energy consumption) - EG.FEC.RNEW.ZS**
3. Deforestation rates/emissions:
    - Carbon dioxide (CO2) net fluxes from LULUCF - Deforestation (Mt CO2e) - EN.GHG.CO2.LU.DF.MT.CE.AR5
4. Water stress levels:
    - **Level of water stress: freshwater withdrawal as a proportion of available freshwater resources - ER.H2O.FWST.ZS**
5. Waste equivalent emissions:
    - **Carbon dioxide (CO2) emissions from Waste (Mt CO2e) - EN.GHG.CO2.WA.MT.CE.AR5**
6. Health expenditure:
    - Current health expenditure (% of GDP) - SH.XPD.CHEX.GD.ZS
    - **Current health expenditure per capita (current US$) - SH.XPD.CHEX.PC.CD**
7. Air pollution:
    - Mortality rate attributed to household and ambient air pollution, age-standardized (per 100,000 population) - SH.STA.AIRP.P5
    - PM2.5 air pollution, population exposed to levels exceeding WHO guideline value (% of total) - EN.ATM.PM25.MC.ZS
    - **PM2.5 air pollution mean annual exposure (micrograms per cubic meter) - EN.ATM.PM25.MC.M3**
8. Education efficiency:
    - Literacy rate, adult total (% of people ages 15 and above) - SE.ADT.LITR.ZS
    - Government expenditure on education, total (% of government expenditure) - SE.XPD.TOTL.GB.ZS
    - **School enrollment, primary (% gross) - SE.PRM.ENRR**
9. Carbon intensity (emissions per GDP):
    - Carbon intensity of GDP (kg CO2e per 2021 PPP) - EN.GHG.CO2.RT.GDP.PP.KD
    - **Carbon intensity of GDP (kg CO2e per constant 2015 US$ of GDP) - EN.GHG.CO2.RT.GDP.KD**
10. Green tech, Investments, R&D:
    - Research and development expenditure (% of GDP) - GB.XPD.RSDV.GD.ZS
    - Patent applications, residents - IP.PAT.RESD
    - **GDP growth (annual %) - NY.GDP.MKTP.KD.ZG**
11. Climate Risk, Droughts, Floods, extreme temperatures
    - Disaster risk reduction progress score (1-5 scale), 5 best - EN.CLC.DRSK.XQ
    - Droughts, floods, extreme temperatures (% of population, average 1990-2009) - EN.CLC.MDAT.ZS 
12. Natural Resource Depletion
    - Adjusted savings: natural resources depletion (% of GNI) - NY.ADJ.DRES.GN.ZS  

### DS02: Data on CO2 and Greenhouse Gas Emissions by Our World in Data
* Metadata URL: https://github.com/owid/co2-data/blob/master/owid-co2-codebook.csv 
* Data URL: https://github.com/owid/co2-data/blob/master/owid-co2-data.csv 
* Data Type: CSV (XlSX, JSON)

*Our World in Data* (OWID) is a non-profit research initiative that makes knowledge accessible and understandable by providing datasets, reports and case studies. The datasets originate from various organizations (UN, WHO, World Bank etc.) and cover a wide range of topics. The datasets are publicly available under Creative Commons BY licenses. The usage of the data is allowed, as long as the source and authors are credited. OWID provides a [guideline](https://ourworldindata.org/faqs#citing-work-produced-by-third-parties-and-made-available-by-our-world-in-data) on how to cite the data. 
Reference:
- Hannah Ritchie, Pablo Rosado and Max Roser (2023) - “CO₂ and Greenhouse Gas Emissions” Published online at OurWorldinData.org. Retrieved from: 'https://ourworldindata.org/co2-and-greenhouse-gas-emissions' [Online Resource]

**List of indicators**
1. Emissions per capita
    - cement_co2_per_capita 
    - co2_including_luc_per_capita  
    - co2_per_capita
    - coal_co2_per_capita  
    - consumption_co2_per_capita  
    - flaring_co2_per_capita  
    - gas_co2_per_capita  
    - ghg_excluding_lucf_per_capita  
    - ghg_per_capita  
    - methane_per_capita  
    - nitrous_oxide_per_capita  
    - oil_co2_per_capita 
    - other_co2_per_capita  
2. Renewable energy share
    - primary_energy_consumption  
    - energy_per_capita  
3. Deforestation rates/emissions
    - cumulative_luc_co2  
    - land_use_change_co2
    - **land_use_change_co2_per_capita**  
    - share_global_luc_co2  
    - share_global_cumulative_luc_co2  
4. Water stress levels
    - 
5. Waste equivalent emissions
    -   
6. Health expenditure
    -  
7. Air pollution
    - methane  
    - nitrous_oxide  
    - temperature_change_from_ch4  
    - temperature_change_from_n2o  
8. Education efficiency
    -  
9. Carbon intensity (emissions per GDP)
    - co2_including_luc_per_gdp  
    - co2_per_gdp  
    - consumption_co2_per_gdp  
    - energy_per_gdp  
10. Green tech, Investments, R&D
    -   
11. Climate Risk, Droughts, Floods, extreme temperatures
    -   
12. Natural Resource Depletion
    - 

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

## Notes
- ASCOR framework for economic indicators 
- NGFS for open data 
- Investments in green/ sustainable technologies
- Investments in clean energy
- Aqueduct for water stress levels