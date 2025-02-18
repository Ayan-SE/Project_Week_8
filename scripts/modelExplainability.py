import lime
import lime.lime_tabular
import pandas as pd
import matplotlib.pyplot as plt

def create_lime_explainer(training_data, feature_names, class_names):
    """Creates and returns a LimeTabularExplainer."""
    explainer = lime.lime_tabular.LimeTabularExplainer(
        training_data=training_data,
        feature_names=feature_names,
        class_names=class_names,
        mode="classification"  
    )
    return explainer

def explain_instance(explainer, instance, predict_fn, num_features=5):
    """Explains a single instance using the provided explainer."""
    explanation = explainer.explain_instance(
        data_row=instance,
        predict_fn=predict_fn,
        num_features=num_features
    )
    return explanation

def plot_feature_importance(explanation, title="LIME Feature Importance"):
    """Plots feature importance from a LIME explanation."""
    feature_weights = dict(explanation.as_list())
    feature_names = list(feature_weights.keys())
    weights = list(feature_weights.values())

    plt.figure(figsize=(10, 6))
    plt.barh(feature_names, weights)
    plt.xlabel("Importance")
    plt.title(title)
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()

def display_explanation(explanation, show_in_notebook=False, save_path=None):
    """Displays or saves the LIME explanation."""
    if show_in_notebook:
        explanation.show_in_notebook(show_all=False)
    else:
        explanation.as_pyplot_figure()  
        import matplotlib.pyplot as plt
        plt.show() 

    print(explanation.as_list())  


