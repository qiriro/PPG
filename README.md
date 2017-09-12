[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)][repository]
[![Python](https://img.shields.io/badge/python-2.7-blue.svg)][python]
[![License](https://img.shields.io/github/license/iRB-Lab/PPG.svg)][license]
[![Watchers](https://img.shields.io/github/watchers/iRB-Lab/PPG.svg?style=social&label=Watch)][watch]
[![Stargazers](https://img.shields.io/github/stars/iRB-Lab/PPG.svg?style=social&label=Star)][star]
[![Forks](https://img.shields.io/github/forks/iRB-Lab/PPG.svg?style=social&label=Fork)][fork]

# PPG
Photoplethysmogram-based Real-Time Cognitive Load Assessment Using Multi-Feature Fusion Model

## Installation
### Requirements
- [macOS][macos] (Recommended)
- [Python 2.7][python]
- [Pip][pip]
- [Virtualenv][virtualenv]

### Installing with Virtualenv
On Unix, Linux, BSD, macOS, and Cygwin:

```sh
git clone https://github.com/iRB-Lab/PPG.git
cd PPG
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Quick Start
On Unix, Linux, BSD, macOS, and Cygwin:

```sh
./scripts/process_data.sh
./scripts/classify.sh
```

## Usage
### Data Processing
##### Raw data segmentation
```sh
python segment.py
```

##### Preprocessing
```sh
python preprocess.py
```

##### Feature extraction
```sh
python extract.py
```

##### Training set and test set spliting
```sh
python split.py
```

### Classification
```sh
python classify.py
```

## Data Definition
### PPG Signal Data
- **Location:** `data/raw/`
- **Filename format:** `<participant>-<label>.txt`

###### Sample Data
```
109
110
109
109
...
```

### Segmented Signal Data
- **Location:** `data/segmented/`
- **Filename format:** `<participant>.json`

###### Sample Data
```js
{
  "<label>": {
    "sample_rate": <value>,
    "signal": [ ... ]
  },
  ...
}
```

### Preprocessed Data
- **Location:** `data/preprocessed/`
- **Filename format:** `<participant>.json`

###### Sample Data
```js
{
  "<label>": {
    "sample_rate": <value>,
    "single_waveforms": [
      [ ... ],
      ...
    ]
  },
  ...
}
```

### Extracted Feature Data
- **Location:** `data/extracted/`
- **Filename format:** `<participant>.json`

###### Sample Data
```js
{
  "<label>": {
    "sample_rate": <value>,
    "ppg45": [
        [ ... ],
        ...
    ],
    "svri": [ ... ]
  },
  ...
}
```

### Splited Feature Data
- **Location:** `data/splited/`
- **Filename format:** `<participant>.json`

###### Sample Data
```js
{
  "train": {
    "<label>": [
      {
        "ppg45": [
          [ ... ],
          ...
        ],
        "svri": [ ... ]
      },
      ...
    ],
    ...
  },
  "test": { ... }
}
```

## Sensors and Features
|Sensor|Feature|Dimension|
|:--|:--|:-:|
|PPG finger clip|PPG-45 (39 time-domain, 9 frequency-domain)|45|
||Stress-induced vascular response index (sVRI)|1|

### PPG-45 Feature Definition
|#|Feature|Description|
|--:|:--|:--|
|1|`x`|Systolic peak|
|2|`y`|Diastolic peak|
|3|`z`|Dicrotic notch|
|4|<code>t<sub>pi</sub></code>|Pulse interval|
|5|`y/x`|Augmentation index|
|6|`(x-y)/x`|Relative augmentation index|
|7|`z/x`||
|8|`(y-z)/x`||
|9|<code>t<sub>1</sub></code>|Systolic peak time|
|10|<code>t<sub>2</sub></code>|Diastolic peak time|
|11|<code>t<sub>3</sub></code>|Dicrotic notch time|
|12|`∆T`|Time between systolic and diastolic peaks|
|13|`w`|Full width at half systolic peak|
|14|<code>A<sub>2</sub>/A<sub>1</sub></code>|Inflection point area ratio|
|15|<code>t<sub>1</sub>/x</code>|Systolic peak rising slope|
|16|<code>y/(t<sub>pi</sub>-t<sub>3</sub>)</code>|Diastolic peak falling slope|
|17|<code>t<sub>1</sub>/t<sub>pi</sub></code>||
|18|<code>t<sub>2</sub>/t<sub>pi</sub></code>||
|19|<code>t<sub>3</sub>/t<sub>pi</sub></code>||
|20|<code>∆T/t<sub>pi</sub></code>||
|21|<code>t<sub>a1</sub></code>||
|22|<code>t<sub>b1</sub></code>||
|23|<code>t<sub>e1</sub></code>||
|24|<code>t<sub>f1</sub></code>||
|25|<code>b<sub>2</sub>/a<sub>2</sub></code>||
|26|<code>e<sub>2</sub>/a<sub>2</sub></code>||
|27|<code>(b<sub>2</sub>+e<sub>2</sub>)/a<sub>2</sub></code>||
|28|<code>t<sub>a2</sub></code>||
|29|<code>t<sub>b2</sub></code>||
|30|<code>t<sub>a1</sub>/t<sub>pi</sub></code>||
|31|<code>t<sub>b1</sub>/t<sub>pi</sub></code>||
|32|<code>t<sub>e1</sub>/t<sub>pi</sub></code>||
|33|<code>t<sub>f1</sub>/t<sub>pi</sub></code>||
|34|<code>t<sub>a2</sub>/t<sub>pi</sub></code>||
|35|<code>t<sub>b2</sub>/t<sub>pi</sub></code>||
|36|<code>(t<sub>a1</sub>+t<sub>a2</sub>)/t<sub>pi</sub></code>||
|37|<code>(t<sub>b1</sub>+t<sub>b2</sub>)/t<sub>pi</sub></code>||
|38|<code>(t<sub>e1</sub>+t<sub>2</sub>)/t<sub>pi</sub></code>||
|39|<code>(t<sub>f1</sub>+t<sub>3</sub>)/t<sub>pi</sub></code>||
|40|<code>f<sub>base</sub></code>|Fundamental component frequency|
|41|<code>\|s<sub>base</sub>\|</code>|Fundamental component magnitude|
|42|<code>f<sub>2</sub></code>|2<sup>nd</sup> harmonic frequency|
|43|<code>\|s<sub>2</sub>\|</code>|2<sup>nd</sup> harmonic magnitude|
|44|<code>f<sub>3</sub></code>|3<sup>rd</sup> harmonic frequency|
|45|<code>\|s<sub>3</sub>\|</code>|3<sup>rd</sup> harmonic magnitude|

## API Reference
### Module: `ppg`
Excerpt from `ppg/__init__.py`:

```python
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
```

### Module: `ppg.params`
Excerpt from `ppg/params.py`:

```python
MINIMUM_PULSE_CYCLE = 0.5
MAXIMUM_PULSE_CYCLE = 1.2

PPG_SAMPLE_RATE = 200
PPG_FIR_FILTER_TAP_NUM = 200
PPG_FILTER_CUTOFF = [0.5, 5.0]
PPG_SYSTOLIC_PEAK_DETECTION_THRESHOLD_COEFFICIENT = 0.5

TRAINING_DATA_RATIO = 0.75
```

### Module: `ppg.signal`
##### Peak Finding
```python
extrema = find_extrema(signal)
```

##### PPG Signal Smoothing
```python
smoothed_ppg_signal = smooth_ppg_signal(
    signal,
    sample_rate=PPG_SAMPLE_RATE,
    numtaps=PPG_FIR_FILTER_TAP_NUM,
    cutoff=PPG_FILTER_CUTOFF
)
```

##### PPG Single-Waveform Validation
```python
result = validate_ppg_single_waveform(single_waveform, sample_rate=PPG_SAMPLE_RATE)
```

##### PPG Single-Waveform Extraction
```python
single_waveforms = extract_ppg_single_waveform(signal, sample_rate=PPG_SAMPLE_RATE)
```

### Module: `ppg.feature`
#### PPG Features
##### PPG-45
```python
extract_ppg45(single_waveform, sample_rate=PPG_SAMPLE_RATE)
```

##### Stress-Induced Vascular Response Index (sVRI)
```python
svri = extract_svri(single_waveform)
```

### Module: `ppg.learn`
##### Split Data Set
```python
train_data, test_data = split_data_set(data, ratio)
```

##### Get Feature Set
```python
train_features, train_labels, test_features, test_labels = get_feature_set(data, label_set, feature_type_set)
```

#### Classifiers
##### Logistic Regression Classifier
```python
classifier = logistic_regression_classifier(features, labels)
```

##### Support Vector Classifier
```python
classifier = support_vector_classifier(features, labels)
```

##### Gaussian Naïve Bayes Classifier
```python
classifier = gaussian_naive_bayes_classifier(features, labels)
```

##### Decision Tree Classifier
```python
classifier = decision_tree_classifier(features, labels)
```

##### Random Forest Classifier
```python
classifier = random_forest_classifier(features, labels)
```

##### AdaBoost Classifier
```python
classifier = adaboost_classifier(features, labels)
```

##### Gradient Boosting Classifier
```python
classifier = gradient_boosting_classifier(features, labels)
```

##### Voting Classifier
```python
classifier = voting_classifier(estimators, features, labels)
```

### Module: `ppg.utils`
```python
make_dirs_for_file(pathname)
```
```python
boolean = exist_file(pathname, overwrite=False, display_info=True)
```
```python
text_data = load_text(pathname, display_info=True)
```
```python
json_data = load_json(pathname, display_info=True)
```
```python
dump_json(data, pathname, overwrite=False, display_info=True)
```
```python
classifier_object = load_model(pathname, display_info=True)
```
```python
dump_model(model, pathname, overwrite=False, display_info=True)
```
```python
export_csv(data, fieldnames, pathname, overwrite=False, display_info=True)
```
```python
datetime = parse_iso_time_string(timestamp)
```
```python
set_matplotlib_backend(backend=None)
```
```python
plot(args, backend=None)
```
```python
semilogy(args, backend=None)
```

## File Structure
```
├── data/
│   ├── raw/
│   │   ├── <participant>-<session_id>-<block_id>-<task_level>.json
│   │   └── ...
│   ├── segmented/
│   │   ├── <participant>.json
│   │   └── ...
│   ├── preprocessed/
│   │   ├── <participant>.json
│   │   └── ...
│   └── extracted/
│       ├── <participant>.json
│       └── ...
├── models/
│   └── ...
├── results/
│   └── ...
├── ppg/
│   ├── __init__.py
│   ├── params.py
│   ├── signal.py
│   ├── feature.py
│   ├── learn.py
│   └── utils.py
├── scripts/
│   ├── process_data.sh
│   └── classify.sh
├── segment.py
├── preprocess.py
├── extract.py
├── split.py
├── classify.py
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

## License
[MIT License][license]

[repository]: https://github.com/iRB-Lab/PPG "iRB-Lab/PPG"
[license]: https://github.com/iRB-Lab/PPG/LICENSE "License"
[watch]: https://github.com/iRB-Lab/PPG/watchers "Watchers"
[star]: https://github.com/iRB-Lab/PPG/stargazers "Stargazers"
[fork]: https://github.com/iRB-Lab/PPG/network "Forks"

[macos]: https://www.apple.com/macos/ "macOS"
[python]: https://docs.python.org/2/ "Python 2.7"
[pip]: https://pypi.python.org/pypi/pip "Pip"
[virtualenv]: https://virtualenv.pypa.io/en/stable/ "Virtualenv"
