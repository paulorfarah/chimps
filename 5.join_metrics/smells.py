import pandas as pd


def join_smells(project_name, current_hash):
    print("Code smells")
    csv_path = '../4.smells/results/' + project_name + '-methods-results.csv'

    metrics = ["projectName", "commitNumber", "fullyQualifiedName",
                          "PublicFieldCount", "IsAbstract", "ClassLinesOfCode", "WeighOfClass",
                          "FANIN", "TightClassCohesion", "FANOUT", "OverrideRatio", "LCOM3",
                          "WeightedMethodCount", "LCOM2", "NumberOfAccessorMethods",
                          'LazyClass', 'DataClass', 'ComplexClass', 'SpaghettiCode',
                          'SpeculativeGenerality', 'GodClass', 'RefusedBequest',
                          'ClassDataShouldBePrivate', 'BrainClass', 'TotalClass',
                          'LongParameterList', 'LongMethod', 'FeatureEnvy',
                          'DispersedCoupling', 'MessageChain', 'IntensiveCoupling',
                          'ShotgunSurgery', 'BrainMethod', 'TotalMethod', 'TotalClassMethod',
                          "DiversityTotal", "DiversityMethod", "DiversityClass"]

    df = pd.read_csv(csv_path, usecols=metrics, sep=',', engine='python', index_col=False)
    df = df[(df['commitNumber'] == current_hash)]

    print(df.shape[0])

    return df
