import warnings
from causalnex.structure import StructureModel
import pandas as pd
from causalnex.structure.notears import from_pandas
import networkx as nx
from causalnex.network import BayesianNetwork
from sklearn.model_selection import train_test_split
from causalnex.evaluation import classification_report
from causalnex.evaluation import roc_auc
from causalnex.inference import InferenceEngine
import numpy as np



warnings.filterwarnings("ignore")  # silence warnings

sm = StructureModel()

data = pd.read_csv('causal_test_data.csv', delimiter=',')
data.columns = data.columns.astype(str)
drop_col = ['code', '01003']
data = data.drop(columns=drop_col)
data.columns = ['col_' + col for col in data.columns]

struct_data = data.copy()
sm = from_pandas(struct_data)
sm.remove_edges_from([(u, v) for u, v, w in sm.edges(data="weight") if w is None or abs(w) < 6])
sm = sm.get_largest_subgraph()
nx.drawing.nx_pydot.write_dot(sm, 'final_graph.dot')

bn = BayesianNetwork(sm)

discretised_data = data.copy()
data_vals = {col: data[col].unique() for col in data.columns}
for col in data.columns:
    
    # 각 컬럼의 30%와 70% 백분위 계산
    q30 = data[col].quantile(0.3)
    q70 = data[col].quantile(0.7)

    # 'col_target'의 분위수 값을 저장
    if col == 'col_target':
        target_q30 = q30
        target_q70 = q70

    # 해당 컬럼에 대한 범주화 맵 생성
    col_map = {
        v: 0 if v <= q30 
        else 1 if v <= q70 
        else 2 for v in data_vals[col]}

    # 범주화 맵 적용
    discretised_data[col] = discretised_data[col].map(col_map)

# 저장된 target_q30과 target_q70을 이용하여 'col_target'의 각 범주별 평균값 계산
mean_0_30 = data['col_target'][data['col_target'] <= target_q30].mean()
mean_30_70 = data['col_target'][(data['col_target'] > target_q30) & (data['col_target'] <= target_q70)].mean()
mean_70_100 = data['col_target'][data['col_target'] > target_q70].mean()

col_target_means = {0: mean_0_30, 1: mean_30_70, 2: mean_70_100}




train, test = train_test_split(discretised_data, train_size=0.9, test_size=0.1, random_state=7)

bn = bn.fit_node_states(discretised_data)
bn = bn.fit_cpds(train, method="BayesianEstimator", bayes_prior="K2")



roc, auc = roc_auc(bn, test, "col_target")
print("\n")
print("The AUC value for our model is ", auc)

c_report = classification_report(bn, test, "col_target")
print("\n")
print(c_report)


bn = bn.fit_cpds(discretised_data, method="BayesianEstimator", bayes_prior="K2")

ie = InferenceEngine(bn)


marginal_1 = ie.query()["col_target"]
print("\n")
print("기존 청년 전출입 비율", marginal_1)

ie.do_intervention("col_08000", {0: 1.0, 1: 0.0, 2: 0.0})
ie.do_intervention("col_22000", {0: 1.0, 1: 0.0, 2: 0.0})
ie.do_intervention("col_26000", {0: 1.0, 1: 0.0, 2: 0.0})


marginal_2 = ie.query()["col_target"]
print("조건 변경시 예상 청년 전출입 비율", marginal_2)
ie.reset_do("col_08000")
ie.reset_do("col_22000")
ie.reset_do("col_26000")



a9 = (marginal_2[2]-marginal_1[2])/marginal_1[2]*100
print("\n")
print("정년 전출입 예상 효용 증가율은 ", a9, "% 입니다.")