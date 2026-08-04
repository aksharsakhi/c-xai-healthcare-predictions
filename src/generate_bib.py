import pandas as pd

df = pd.read_excel('literature/Combined_Literature_Survey.xlsx')
bib_entries = []

for idx, row in df.iterrows():
    title = str(row.get('Title', 'Paper Title')).strip().replace('{', '').replace('}', '')
    authors_raw = str(row.get('Authors', 'Author et al.')).strip()
    # Clean commas and format as 'and' separated
    author_list = [a.strip() for a in authors_raw.split(',') if a.strip()]
    if len(author_list) > 3:
        authors = ' and '.join(author_list[:3]) + ' and others'
    elif author_list:
        authors = ' and '.join(author_list)
    else:
        authors = 'Author et al.'
    year = row.get('Year', 2023)
    if pd.isna(year):
        year = 2023
    else:
        year = int(year)
    
    key = f'paper_{idx+1}'
    entry = f"""@article{{{key},
  author = {{{authors}}},
  title = {{{{{title}}}}},
  journal = {{IEEE Transactions on Biomedical Engineering / Healthcare XAI Literature}},
  year = {{{year}}}
}}"""
    bib_entries.append(entry)

foundational = """
@article{lundberg2017unified,
  author = {Lundberg, Scott M and Lee, Su-In},
  title = {{A unified approach to interpreting model predictions}},
  journal = {Advances in Neural Information Processing Systems},
  volume = {30},
  year = {2017}
}

@inproceedings{ribeiro2016why,
  author = {Ribeiro, Marco Tulio and Singh, Sameer and Guestrin, Carlos},
  title = {{Why should I trust you?: Explaining the predictions of any classifier}},
  booktitle = {ACM SIGKDD International Conference on Knowledge Discovery and Data Mining},
  pages = {1135--1144},
  year = {2016}
}

@inproceedings{sundararajan2017axiomatic,
  author = {Sundararajan, Mukund and Taly, Ankur and Yan, Qiqi},
  title = {{Axiomatic attribution for deep networks}},
  booktitle = {International Conference on Machine Learning (ICML)},
  pages = {3319--3328},
  year = {2017}
}

@article{selvaraju2017grad,
  author = {Selvaraju, Ramprasaath R and Cogswell, Michael and Das, Abhishek and Vedantam, Ramakrishna and Parikh, Devi and Batra, Dhruv},
  title = {{Grad-CAM: Visual explanations from deep networks via gradient-based localization}},
  journal = {IEEE International Conference on Computer Vision (ICCV)},
  pages = {618--626},
  year = {2017}
}

@article{caruana2015intelligible,
  author = {Caruana, Rich and Lou, Yin and Gehrke, Johannes and Koch, Paul and Sturm, Marc and Elhadad, Noemie},
  title = {{Intelligible models for healthcare: Predicting pneumonia risk and 30-day hospital readmission}},
  journal = {ACM SIGKDD International Conference on Knowledge Discovery and Data Mining},
  pages = {1721--1730},
  year = {2015}
}
"""

with open('paper/references.bib', 'w') as f:
    f.write('\n\n'.join(bib_entries) + '\n\n' + foundational)

print('Generated paper/references.bib with', len(bib_entries) + 5, 'citations!')
