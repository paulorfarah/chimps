from sklearn.neural_network import MLPClassifier
from sklearn.inspection import permutation_importance
import matplotlib.pyplot as plt
import pandas as pd
import glob
import os

from main import get_main_columns


def feature_importance(X, y):
    # Suponha X, y já definidos (features e target)
    model = MLPClassifier(hidden_layer_sizes=(10,), random_state=1)
    model.fit(X, y)

    # Calcula a importância por permutação com 10 repetições
    result = permutation_importance(model, X, y, n_repeats=10, random_state=1)

    # A importância média das features
    importance_means = result.importances_mean
    # Ordena as features pela importância
    sorted_idx = importance_means.argsort()

    # Plota a importância
    plt.rcParams['figure.figsize'] = (14, 18)  # Set default size for all new figures

    plt.barh(range(len(sorted_idx)), importance_means[sorted_idx])
    plt.yticks(range(len(sorted_idx)), [X.columns[i] for i in sorted_idx])
    plt.xlabel("Importância por Permutação")
    plt.title("Feature Importance para MLPClassifier")

    plt.savefig("results/feature_importance.pdf")


if __name__ == '__main__':
    feature_names = get_main_columns()
    path = 'data'
    all_files = glob.glob(os.path.join(path, "*.csv"))

    df = pd.DataFrame()
    for f in all_files:
        df_new = pd.read_csv(f)
        df_new.columns = feature_names
        # Concatenate along rows (axis=0) to add new rows
        df = pd.concat([df, df_new], ignore_index=True)
        print(f)
        print(df.shape)

    # df = pd.concat((pd.read_csv(f) for f in all_files), ignore_index=True)
    print(df.shape)

    df.columns = feature_names
    df = df.fillna(0)

    y_shap = df['will_change']


    categorical_features = ["project", "commit", "TOTAL_CHANGES", "release", "will_change", "file",
                                                  "class", "method", "constructor", "line", "method_name", "current_hash",
                                                  "Name", "File", "commitprevious", "file", "method", "PROJECT_NAME",
                                                  "PREVIOUS_COMMIT", "CURRENT_COMMIT", "CLASS_CURRENTCOMMIT", "CLASS_PREVIOUSCOMMIT",
                                                  "CLASS_CURRENTNAME", "CLASS_PREVIOUSNAME", "hasJavaDoc", "Kind", ]
    change_features = [
                        "STATEMENT_DELETE", "STATEMENT_INSERT", "STATEMENT_ORDERING_CHANGE",
                        "STATEMENT_PARENT_CHANGE", "STATEMENT_UPDATE", "TOTAL_STATEMENTLEVELCHANGES",
                        "PARENT_CLASS_CHANGE", "PARENT_CLASS_DELETE", "PARENT_CLASS_INSERT", "CLASS_RENAMING",
                        "TOTAL_CLASSDECLARATIONCHANGES",
                        "RETURN_TYPE_CHANGE", "RETURN_TYPE_DELETE", "RETURN_TYPE_INSERT", "METHOD_RENAMING",
                        "PARAMETER_DELETE", "PARAMETER_INSERT", "PARAMETER_ORDERING_CHANGE", "PARAMETER_RENAMING",
                        "PARAMETER_TYPE_CHANGE", "TOTAL_METHODDECLARATIONSCHANGES",
                        "ATTRIBUTE_RENAMING", "ATTRIBUTE_TYPE_CHANGE", "TOTAL_ATTRIBUTEDECLARATIONCHANGES",
                        "ADDING_ATTRIBUTE_MODIFIABILITY", "REMOVING_ATTRIBUTE_MODIFIABILITY",
                        "REMOVING_CLASS_DERIVABILITY", "REMOVING_METHOD_OVERRIDABILITY",
                        "ADDING_CLASS_DERIVABILITY", "ADDING_CLASS_DERIVABILITY", "ADDING_METHOD_OVERRIDABILITY",
                        "TOTAL_DECLARATIONPARTCHANGES"]
    X_shap = df.drop(columns=categorical_features)
    X_shap = X_shap.drop(columns=change_features)
    for feature in categorical_features:
        feature_names.remove(feature)
    for feature in change_features:
        feature_names.remove(feature)


    # X_train, X_test, y_train, y_test = train_test_split(
    #     X_shap, y_shap, test_size=0.30, random_state=42)
    feature_importance(X_shap, y_shap)