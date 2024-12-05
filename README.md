# 인구감소지역 시뮬레이션 도구

![image](https://github.com/user-attachments/assets/35112fd8-bd8c-4a29-ba5e-95bd8c2f39ef)


**Python 기반의 시뮬레이션 도구로, 인구 감소 및 청년 전출입 데이터를 분석하고 예측합니다.**  
국가통계포털(KOSIS) 및 국토교통부 데이터를 활용하여 인과 네트워크를 구성하고, 전출입 예측 및 개입 효과를 분석할 수 있습니다.

---

## 주요 기능
- **데이터 전처리**: 불필요한 컬럼 제거 및 재구성
- **인과 네트워크 생성**: 데이터를 기반으로 인과 관계를 시각화
- **전출입 예측**: ROC-AUC 값을 활용한 모델 성능 평가
- **개입 효과 분석**: 특정 변수 개입 시 예상 결과 비교

---

## 시스템 요구사항
- **운영체제**: Windows 11 Pro
- **Python 버전**: 3.8.20 (Anaconda 가상환경)
- **필수 라이브러리**:
  - warnings
  - pandas
  - networkx
  - causalnex
  - sklearn
  - matplotlib
  - numpy

---

## 설치 방법

1. **Python 및 Anaconda 설치**
   - Python 3.8.20 버전 설치
   - [Anaconda 다운로드](https://www.anaconda.com/)

2. **가상환경 구성**
   ```bash
   conda create -n causalnex_env python=3.8.20
   conda activate causalnex_env
   ```

3. **필요한 라이브러리 설치**
   ```bash
   pip install pandas networkx causalnex scikit-learn matplotlib numpy
   ```

4. **프로젝트 파일 다운로드**
   - 프로젝트 디렉토리에 `network_prediction.py`, `network_visualization.py`와 데이터 파일(`causal_test_data.csv`)을 포함시킵니다.

---

## 데이터 파일 구조

### 입력 데이터: `causal_test_data.csv`
- **주요 컬럼**:
  - `region`: 지역명
  - `age_group`: 연령 그룹 (미성년, 청년, 중년, 노년)
  - `population`: 인구 수
  - `building_type`: 건물 용도별 정보
  - `migration`: 전출입 데이터

---

## 실행 방법

1. **전출입 예측 실행**
   - Anaconda Prompt에서 프로젝트 디렉토리로 이동합니다:
     ```bash
     cd H:\TTA_Test2024
     ```
   - `network_prediction.py` 실행:
     ```bash
     python network_prediction.py
     ```

2. **인과 네트워크 시각화**
   - 인과 네트워크 구조를 시각화하기 위해 다음 명령어를 실행합니다:
     ```bash
     python network_visualization.py
     ```

---

## 코드 설명

### 데이터 로드 및 전처리
```python
data = pd.read_csv('causal_test_data.csv')
data = preprocess_data(data)  # 불필요한 컬럼 제거 및 컬럼 이름 조정
```

### 인과 네트워크 생성
```python
sm = create_structure_model(data)  # 데이터 기반의 인과 그래프 생성
save_structure_graph(sm, 'final_graph.dot')  # DOT 파일로 저장
```

### 베이지안 네트워크 학습 및 평가
```python
bn = BayesianNetwork(sm)
train, test = train_test_split(data, train_size=0.9)
bn = bn.fit_cpds(train)
roc, auc = roc_auc(bn, test, "col_target")
```

---

## 결과 확인

- **AUC 값**: 0.6 이상
- **예상 효용 증가율**: 10% 이상
- **시각화 파일**: `final_graph.dot` 파일 생성 후 시각화를 통해 네트워크 구조를 확인합니다.

---

## 참고 자료
- [국가통계포털(KOSIS)](https://kosis.kr)
- [국토교통부](https://www.molit.go.kr)

---

## 라이선스
이 프로젝트는 [Apache License 2.0](LICENSE)을 따릅니다.
