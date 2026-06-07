import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import shap

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
# from sklearn.datasets import make_classification

import pandas as pd
import glob
import os

from main import get_main_columns


def generate_shap_charts(X_train, X_test, y_train, y_test, feature_names):
    # ===============================
    # 3. Pipeline com Scaler + MLP
    # ===============================
    model = Pipeline([
        ("scaler", StandardScaler()),
        # ("clf", MLPClassifier(hidden_layer_sizes=(50, 25),
        #                       activation="relu", solver="adam",
        #                       max_iter=1000, random_state=42))
        ("clf", MLPClassifier(random_state=42)),
    ])

    # ===============================
    # 4. Validação cruzada (10 folds)
    # ===============================
    cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
    scores = cross_val_score(model, X_train, y_train, cv=cv, scoring="accuracy")

    print("Validação cruzada (10 folds) - Acurácia por fold:", scores)
    print("Média de acurácia (treino):", np.mean(scores))

    # ===============================
    # 5. Treinar no conjunto de treino
    # ===============================
    model.fit(X_train, y_train)

    # ===============================
    # 6. Avaliar no conjunto de teste
    # ===============================
    y_pred = model.predict(X_test)

    print("\nAcurácia no teste:", accuracy_score(y_test, y_pred))
    print("\nRelatório de classificação:\n", classification_report(y_test, y_pred))

    # ===============================
    # 7. SHAP Analysis
    # ===============================
    scaler = model.named_steps["scaler"]
    clf = model.named_steps["clf"]

    X_train_scaled = scaler.transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Amostra de background para acelerar
    background = shap.utils.sample(X_train_scaled, 100, random_state=42)

    # 🔧 Explainer para a classe positiva (probabilidade)
    explainer = shap.KernelExplainer(lambda x: clf.predict_proba(x)[:,1], background)

    # Selecionamos só 200 amostras de teste
    X_test_sample = X_test_scaled[:200]

    # Calcular SHAP
    shap_values = explainer.shap_values(X_test_sample, nsamples=100)

    print("Shapes:", shap_values.shape, X_test_sample.shape)  # deve dar (200, 10) (200, 10)
    print("features: ", len(feature_names))

    # --- Summary Plot ---
    shap.summary_plot(shap_values, X_test_sample, show=False, feature_names=feature_names)
    plt.tight_layout()
    plt.savefig("results/shap/shap_summary1.pdf", dpi=300)
    plt.close()

    # --- Bar Plot ---
    shap_importance = np.mean(np.abs(shap_values), axis=0)
    feature_importance = pd.DataFrame({
         "feature": feature_names,
        "importance": shap_importance
    }).sort_values(by="importance", ascending=False)

    plt.figure(figsize=(8, 24))
    plt.barh(feature_importance["feature"], feature_importance["importance"])
    plt.gca().invert_yaxis()
    plt.xlabel("Average Importance - SHAP")
    plt.title("Feature Ranking - SHAP")
    plt.tight_layout()
    plt.savefig("results/shap/shap_barplot1.pdf", dpi=300)
    plt.close()

    # --- Dependence Plots automáticos para top N features ---
    N = 3  # quantas features você quer analisar em detalhe
    top_features = feature_importance["feature"].head(N).tolist()

    print(f"Gerando dependence plots para top {N} features: {top_features}")

    for feat in top_features:
        shap.dependence_plot(
            feat,
            shap_values,
            X_test_sample,
            feature_names=feature_names,
            show=False
        )
        plt.tight_layout()
        plt.savefig(f"results/shap/shap_dependence_{feat}.pdf", dpi=300)
        plt.close()

    print("\nGráficos salvos: shap_summary.pdf, shap_barplot.pdf e shap_dependence_*.pdf")

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


    X_train, X_test, y_train, y_test = train_test_split(
        X_shap, y_shap, test_size=0.30, random_state=42)

    generate_shap_charts(X_train, X_test, y_train, y_test, feature_names)