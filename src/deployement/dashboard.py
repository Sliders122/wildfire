import pickle
import pandas as pd
from explainerdashboard import ClassifierExplainer, ExplainerDashboard

#load the data
df = pd.read_csv("df_model.csv")

# Split the test data
df_xtest = df.drop(['index','FireMask','time','FireMask_pred','FireMask_proba'], axis=1)
df_ytest = df['FireMask']

#load the model
model_path = open('model_lgbm.pkl' , 'rb')
model = pickle.load(model_path)

# Create and run the dashboard on port 9050
explainer = ClassifierExplainer(model, df_xtest, df_ytest)
ExplainerDashboard(explainer).run(port=9050)