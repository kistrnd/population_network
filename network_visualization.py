import networkx as nx
import matplotlib.pyplot as plt

# .dot 파일에서 그래프 로드 (pydot 사용)
graph = nx.nx_pydot.read_dot("final_graph.dot")

# 엣지 가중치가 문자열인 경우 float로 변환
for u, v, data in graph.edges(data=True):
    if 'weight' in data and isinstance(data['weight'], str):
        data['weight'] = float(data['weight'].replace('"', ''))  # 문자열을 부동소수점 숫자로 변환

# 노드 카테고리 수정 (CSV 파일 열 이름에 맞추어 col_ 접두사를 제거하여 표시)
building_capacity_nodes = {
    "01000", "01003", "02000", "03000", "04000", "05000", "06000", "07000", "08000", "09000",
    "10000", "11000", "12000", "13000", "14000", "15000", "16000", "17000", "18000",
    "19000", "20000", "21000", "22000", "23000", "24000", "25000", "26000", "27000",
    "28000", "29000", "Z3000", "Z5000", "Z6000", "Z8000", "Z9000"
}
age_gender_nodes = {"m_minor", "m_youth", "m_middle", "m_old", "f_minor", "f_youth", "f_middle", "f_old"}
target_nodes = {"target"}

# 각 노드의 위치 설정 (pos 속성이 없으면 spring layout 사용)
positions = {}
for node in graph.nodes():
    if 'pos' in graph.nodes[node]:
        x, y = map(float, graph.nodes[node]['pos'].split(","))
        positions[node] = (x, y)

# spring_layout 또는 shell_layout 시도
if not positions:
    # positions = nx.spring_layout(graph, k=2.0, iterations=200)  # k 값을 크게 설정하여 노드 간 거리 증가
    positions = nx.shell_layout(graph)  # shell_layout으로 노드들을 계층적으로 배치

# 노드 카테고리에 따라 색상 및 크기 설정
node_colors = []
node_labels = {node: node.replace("col_", "") for node in graph.nodes()}  # col_ 접두사 제거
node_sizes = [len(label) * 100 + 200 for label in node_labels.values()]  # 노드 크기 확대

for node in graph.nodes():
    plain_node = node.replace("col_", "")  # col_ 접두사 제거
    if plain_node in building_capacity_nodes:
        node_colors.append('yellow')
    elif plain_node in age_gender_nodes:
        node_colors.append('purple')
    elif plain_node in target_nodes:
        node_colors.append('red')
    else:
        node_colors.append('blue')

# 엣지의 두께와 색상 설정 (가중치에 비례)
edges, edge_colors, edge_widths, edge_labels = [], [], [], {}

# 엣지의 최소/최대 가중치 계산하여 두께 비율(scale_factor) 설정
min_weight = min(abs(float(edge[2].get('weight', 1))) for edge in graph.edges(data=True))
max_weight = max(abs(float(edge[2].get('weight', 1))) for edge in graph.edges(data=True))
scale_factor = 10 / (max_weight - min_weight) if max_weight != min_weight else 1  # 두께 비율 조정

# 엣지 정보 추출
for edge in graph.edges(data=True):
    weight = float(edge[2].get('weight', 1))
    edges.append((edge[0], edge[1]))
    edge_colors.append('#ff9999' if weight < 0 else '#99ccff')  # 부호에 따라 색상 결정
    edge_widths.append(abs(weight) * scale_factor)  # 엣지 두께를 가중치에 비례하게 설정
    edge_labels[(edge[0], edge[1])] = f"{weight:.2f}"  # 엣지에 가중치 값 라벨 설정

# 그래프 그리기
plt.figure(figsize=(15, 15))  # 그림 크기 조정
nx.draw_networkx_nodes(graph, positions, node_color=node_colors, node_size=node_sizes, edgecolors='black')
nx.draw_networkx_labels(graph, positions, labels=node_labels, font_size=8, font_color="black")
nx.draw_networkx_edges(graph, positions, edgelist=edges, edge_color=edge_colors, width=edge_widths)
nx.draw_networkx_edge_labels(graph, positions, edge_labels=edge_labels, font_size=7)

# 범례 표시
import matplotlib.lines as mlines
legend_elements = [
    mlines.Line2D([], [], color='yellow', marker='o', linestyle='None', markersize=10, label='Number of Buildings by Use'),
    mlines.Line2D([], [], color='purple', marker='o', linestyle='None', markersize=10, label='Age/Gender Groups'),
    mlines.Line2D([], [], color='red', marker='o', linestyle='None', markersize=10, label='Target Node'),
    mlines.Line2D([], [], color='blue', marker='o', linestyle='None', markersize=10, label='Other'),
    mlines.Line2D([], [], color='#ff9999', linewidth=2, label='Negative Weight (Red)'),
    mlines.Line2D([], [], color='#99ccff', linewidth=2, label='Positive Weight (Blue)')
]
plt.legend(handles=legend_elements, loc='upper right')

plt.axis('off')  # 축 표시 끄기
plt.show()
