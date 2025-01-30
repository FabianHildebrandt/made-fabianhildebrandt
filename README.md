# SCA 2024 - Sustainability Championship of America 2024

The Sustainability Championship of America 2024 (SCA 2024) presents a comparison of the national sustainability performance of the Americas in three dimensions: environmental, economical, and social. The analysis uses carefully selected comparative indicators that avoid penalizing smaller or economically emerging nations. The analysis introduces two distinct rankings: overall champions demonstrating consistent high performance and rising stars with significant recent improvements. It will also show which countries are latecomers struggling with sustainability challenges.

![Overall champion](./project/figures/Overall%20Champion.png)

# How to get started

1. [Project Report](./project/analysis-report.pdf)
2. [Data Report](./project/data-report.pdf)
3. [Project presentation](./project/presentation-video.md)
4. Full rankings: [Overall champions](./project/data/Overall%20Champion.xlsx), [Rising stars](./project/data/Overall%20Champion.xlsx)
5. [Further visualizations](./project/figures)

# Reproduce the results 

1. Fork and clone the repository.
```bash
git clone https://github.com/FabianHildebrandt/made-fabianhildebrandt.git
```

2. Go to the main directory. 
```bash
cd made-fabianhildebrandt
```

3. Install the requirements
```bash
pip install -r requirements.txt
```

3. Run the pipeline.
```bash
chxmod +x ./project/pipeline.sh
./project/pipeline.sh
```

4. Run the analysis. 
```bash
python ./project/data-analysis.py
```

5. Adjust the [configuration](./project/config.yaml) to do your own experiments. Please note, that you need to adjust the range of the map plots in the data analysis (s. [here](./project/data-analysis.py#L220)) to show other continents.

# License
The visualizations and reports are free and open-source under the CC-BY License.
The data is subject to the license terms from the original third-party authors. The original source of the data is shown in the *LICENSES.xlsx*. Please check the license of any such third-party data before use and redistribution.

![CC-BY 4.0](https://mirrors.creativecommons.org/presskit/buttons/88x31/png/by.png)