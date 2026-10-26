# FAKE NEWS DETECTION USING LSTM
## Course Project Report
**Subject:** AIT-401 – Foundations of Deep Learning  
**Submitted to:** APJ Abdul Kalam Technological University, Kerala  
*For the partial fulfilment of the requirements for the award of the degree of*  
**Bachelor of Technology in COMPUTER SCIENCE AND ENGINEERING (ARTIFICIAL INTELLIGENCE)**

---

### Submitted By:
- **KRISHNA PRIYA V R** — ASI23CA039
- **MAGNEL OLIVERO** — ASI23CA040
- **MILIYA ROSE SEPHY** — ASI23CA041

### Guided By:
**PROF. ASHA ROSE THOMAS**  
*Department of AI & DS*  
**ADI SHANKARA INSTITUTE OF ENGINEERING AND TECHNOLOGY, KALADY**  
*OCTOBER 2026*

---

## CERTIFICATE

This is to certify that the course project report entitled **“Fake News Detection using LSTM”** submitted by **Krishna Priya V R** (ASI23CA039), **Magnel Olivero** (ASI23CA040), and **Miliya Rose Sephy** (ASI23CA041) of Seventh Semester, B.Tech in Computer Science & Engineering (Artificial Intelligence) has been successfully carried out under our supervision and guidance in partial fulfilment of the requirements of the course project for the subject **AIT-401 – Foundations of Deep Learning**, prescribed by APJ Abdul Kalam Technological University, Kerala. It is further certified that this work is a bonafide record of the course project carried out by the above students during the academic year **2026–27**.

- **Prof. Asha Rose** — *Project Guide*
- **Dr. Sarika S** — *Professor and Head, Department of AI and DS*

---

## DECLARATION

We hereby declare that the course project report **“Fake News Detection using LSTM”** submitted for the partial fulfilment of the requirements of the Seventh Semester course project for the subject **AIT-401 – Foundations of Deep Learning**, prescribed by APJ Abdul Kalam Technological University, Kerala, is a bonafide work done by us under the guidance of **Prof. Asha Rose**.

The submission represents our ideas in our own words, and where ideas or words of others have been included, we have adequately and accurately cited and referred to the original sources. We also declare that we have adhered to ethics and integrity and have not misinterpreted or fabricated any data, idea, fact or source in our submission. We understand that any violation of the above will be a case for disciplinary action by the institution and/or the University and can also evoke penal action from the sources which have not been properly cited or from whom proper permission has not been obtained. This report has not previously formed the basis for the award of any degree, diploma or similar title of any other University.

- **KRISHNA PRIYA V R** — ASI23CA039  
- **MAGNEL OLIVERO** — ASI23CA040  
- **MILIYA ROSE SEPHY** — ASI23CA041  

**Place:** Kalady  
**Date:** October 2026

---

## INSTITUTION & DEPARTMENT VISION & MISSION

### Institution Vision
To emerge as a Center of Excellence in Engineering, Technology and Management by imparting quality education, focusing on empowerment and innovation.

### Institution Mission
- Impart quality professional education for total upliftment of the society.
- Create congenial academic ambience that kindles innovative thinking and research.
- Mold competent professionals who are socially committed and responsible citizens.

### Department Vision
To be in the frontier of AI technology through quality of education, collaborative research and produce globally competitive, industry ready engineers with social commitment.

### Department Mission
- Achieve excellence in the educational experience, fostering collaborative research through state-of-the-art infrastructure and innovative elements.
- Establish industry collaboration to address interdisciplinary challenges across diverse applications.
- Inspire students to develop into ethical, innovative and entrepreneurial leaders through a socially-centered program.

---

## PROGRAM SPECIFIC OUTCOMES (PSOs) & PROGRAM OUTCOMES (POs)

### Program Specific Outcomes (PSOs)
- **PSO 1:** Graduates will have the ability to apply data science techniques, including data collection, cleaning, processing, analysis and visualization to extract actionable insights from large, complex datasets across various domains such as business, healthcare, and technology.
- **PSO 2:** Graduates will be proficient in designing, developing and deploying machine learning algorithms and predictive models, utilizing statistical, mathematical and computational techniques to solve real-world problems and enhance decision-making processes.

### Program Outcomes (POs)
1. **Engineering knowledge:** Apply the knowledge of mathematics, science, engineering fundamentals, and an engineering specialization to the solution of complex engineering problems.
2. **Problem analysis:** Identify, formulate, research literature, and analyze complex engineering problems reaching substantiated conclusions using first principles of mathematics, natural sciences, and engineering sciences.
3. **Design/development of solutions:** Design solutions for complex engineering problems and design system components or processes that meet the specified needs with appropriate consideration for public health and safety, and cultural, societal, and environmental considerations.
4. **Conduct investigations of complex problems:** Use research-based knowledge and research methods including design of experiments, analysis and interpretation of data, and synthesis of information to provide valid conclusions.
5. **Modern tool usage:** Create, select, and apply appropriate techniques, resources, and modern engineering and IT tools including prediction and modeling to complex engineering activities with an understanding of limitations.
6. **The engineer and society:** Apply reasoning informed by contextual knowledge to assess societal, health, safety, legal and cultural issues and the consequent responsibilities relevant to professional engineering practice.
7. **Environment and sustainability:** Understand the impact of professional engineering solutions in societal and environmental contexts, and demonstrate knowledge of, and need for sustainable development.
8. **Ethics:** Apply ethical principles and commit to professional ethics and responsibilities and norms of engineering practice.
9. **Individual and team work:** Function effectively as an individual, and as a member or leader in diverse teams, and in multidisciplinary settings.
10. **Communication:** Communicate effectively on complex engineering activities with the engineering community and with society at large.
11. **Project management and finance:** Demonstrate knowledge and understanding of engineering and management principles and apply these to one's own work.
12. **Life-long learning:** Recognize the need for, and have preparation and ability to engage in independent and life-long learning in the broadest context of technological change.

---

## COURSE OUTCOMES (COs) & MAPPING

| CO# | Course Outcome (AIT-401) | Cognitive Knowledge Level |
|---|---|---|
| **CO1** | Illustrate the basic concepts of neural networks, deep learning and its practical issues. | Apply |
| **CO2** | Outline the standard regularization and optimization techniques for the effective training of deep neural networks. | Understand |
| **CO3** | Build convolutional neural network (CNN) models for different use cases. | Apply |
| **CO4** | Apply the concepts of Recurrent Neural Network (RNN), Long Short Term Memory (LSTM), Gated Recurrent Unit (GRU). | Apply |
| **CO5** | Explain the concepts of auto encoder, generative models. | Understand |

### Mapping of this Project to Course Outcomes
| CO# | Addressed in this project through | Chapter |
|---|---|---|
| **CO1** | Embedding, dense layers, sigmoid output and binary cross-entropy; practical issues such as overfitting and data leakage | 3, 4, 5 |
| **CO2** | Dropout, early stopping, mini-batch training and the Adam optimizer | 4, 5 |
| **CO3** | Reviewed as an alternative (1D CNN for text); proposed as an extension, not implemented | 2, 7 |
| **CO4** | Bidirectional LSTM classifier implemented; GRU and plain RNN compared in the review | 2, 3, 4 |
| **CO5** | Autoencoders and generative models discussed, including how generated text makes detection harder | 2, 7 |

---

## ABSTRACT

The rapid spread of misinformation through online news and social media is a serious threat to public discourse, and manual fact-checking cannot keep pace with the volume of content. This project applies deep learning to fake news detection: given the text of a news article, the system classifies it as real or fake.

The pipeline uses standard NLP preprocessing (lowercasing, noise removal, stopword removal and lemmatization), converts articles into padded integer sequences, and feeds them to a **Bidirectional Long Short-Term Memory (BiLSTM)** network with an embedding layer, dropout regularization and a sigmoid output. The model is trained with the Adam optimizer and binary cross-entropy loss, and early stopping is used to control overfitting.

The Kaggle “Fake and Real News” dataset was used. During analysis, a source-specific artifact (the news-agency dateline at the start of real articles, e.g., `"CITY (Reuters) -"`) was found to leak the class label, and it was removed so that the model learns from the language of the articles rather than a shortcut. On a held-out test set of 7,821 articles, the model achieved **99.36% accuracy**, with precision, recall, and F1-score of **0.99** for both classes, misclassifying only 50 articles in total. The project demonstrates neural network fundamentals, regularization and optimization, and recurrent architectures from the course, and it discusses the limits of style-based detection and the need for cross-dataset evaluation.

---

## TABLE OF CONTENTS

1. **Chapter 1: Introduction** ................................................................................................ 1
   - 1.1 Background of the Study
   - 1.2 Need for the Project
   - 1.3 Objectives
   - 1.4 Scope
   - 1.5 Methodology
   - 1.6 Organization of the Report
2. **Chapter 2: Literature Review** ........................................................................................ 4
   - 2.1 Overview of Deep Learning Techniques
   - 2.2 Review of Related Works
   - 2.3 Comparative Study
3. **Chapter 3: System Requirements & Design** .................................................................. 6
   - 3.1 Hardware Requirements
   - 3.2 Software Requirements
   - 3.3 System Architecture
   - 3.4 Module Design
   - 3.5 Flowchart Description
   - 3.6 Model Architecture
   - 3.7 UML Diagrams
4. **Chapter 4: Implementation** .......................................................................................... 9
   - 4.1 Problem Definition
   - 4.2 Dataset Description
   - 4.3 Data Leakage and Its Removal
   - 4.4 Preprocessing Steps
   - 4.5 Tokenization and Sequence Preparation
   - 4.6 Model Implementation (CO1, CO4)
   - 4.7 Regularization and Optimization (CO2)
   - 4.8 Pseudocode
   - 4.9 Data Structures Used
   - 4.10 Sample Input and Output
   - 4.11 Time and Space Complexity Analysis
   - 4.12 Applications
5. **Chapter 5: Results and Performance Analysis** ............................................................ 12
   - 5.1 Experimental Setup
   - 5.2 Training Results
   - 5.3 Test Set Performance
   - 5.4 Graphical Analysis
   - 5.5 Observations
   - 5.6 Threats to Validity
6. **Chapter 6: Conclusion** ................................................................................................. 14
   - 6.1 Summary of Work
   - 6.2 Key Findings
   - 6.3 Learning Outcomes
7. **Chapter 7: Future Enhancements** ............................................................................... 16
   - 7.1 Web Application
   - 7.2 Better Text Representations
   - 7.3 Model Variations (CO3, CO4)
   - 7.4 More Robust Evaluation
   - 7.5 Explainability
   - 7.6 Autoencoders and Generative Models (CO5)
   - 7.7 Multilingual and Multimodal Detection
8. **Chapter 8: References** ................................................................................................. 17
9. **Appendix A: Source Code** ........................................................................................... 19

---

## CHAPTER 1: INTRODUCTION

Fake news detection is the task of deciding automatically whether a news article is genuine or misleading. It is a natural fit for deep learning because the signal lies in the text itself: word choice, sentence style and the order in which words appear. This project builds and evaluates a recurrent neural network (a Bidirectional LSTM) for this task and studies how regularization, optimization and data quality affect the result.

### 1.1 Background of the Study
Online platforms let anyone publish and share information instantly. This has widened access to news, but it has also let false stories reach millions of readers before they can be corrected. Traditional machine learning approaches relied on hand-crafted features such as word counts and n-grams. Deep learning replaces this manual feature work: an embedding layer learns word representations, and a recurrent layer reads the article in order and builds a summary of its content. The LSTM was designed to remember information across long sequences, which makes it suitable for articles that run to hundreds of words.

### 1.2 Need for the Project
The volume of online content makes manual verification impossible at scale. Automated tools are useful for:
- Flagging suspicious articles for human fact-checkers
- Helping platforms reduce the reach of misleading stories
- Supporting media-literacy education by showing which language patterns are common in unreliable sources

A deep learning classifier that is accurate, fast at prediction time and honestly evaluated is a practical first step towards these goals.

### 1.3 Objectives
The main objectives of this project are:
- To understand the basic concepts of neural networks and the practical issues in training them (CO1)
- To apply regularization and optimization techniques such as dropout, early stopping and the Adam optimizer (CO2)
- To design, train and evaluate an LSTM-based classifier for fake news detection (CO4)
- To apply NLP preprocessing to raw news text
- To identify possible bias or data leakage in the dataset and evaluate the model honestly
- To discuss the social relevance and limitations of automated fake news detection

### 1.4 Scope
This project covers the design, implementation and evaluation of a binary text classifier. The scope includes:
- Working with English news articles (title and body text)
- Preprocessing, tokenization and sequence padding
- Training and evaluating a BiLSTM model
- Reporting precision, recall, F1-score and a confusion matrix
- Predicting the label of a new article

However, the project does not cover:
- Verification of individual factual claims against external sources
- Images, video or social-network propagation features
- Multilingual detection
- Transformer-based models and production deployment

### 1.5 Methodology
The project follows a systematic approach:
1. **Problem definition** – Binary classification of articles as real or fake
2. **Data preparation** – Loading the dataset, labelling, removing duplicates and splitting into training and test sets
3. **Preprocessing** – Cleaning and normalizing the text with NLP techniques
4. **Model design** – Embedding, BiLSTM, dropout and dense layers
5. **Training** – Adam optimizer, binary cross-entropy loss and early stopping
6. **Evaluation** – Precision, recall, F1-score, confusion matrix and training curves

### 1.6 Organization of the Report
The report is structured into 8 chapters covering introduction, literature review, design, implementation, performance analysis, conclusion, future enhancements, references, and Appendix A with complete source code.

---

## CHAPTER 2: LITERATURE REVIEW

### 2.1 Overview of Deep Learning Techniques
- **Feedforward neural networks and practical issues:** A network of layers trained by backpropagation. Practical issues include vanishing or exploding gradients, overfitting and poor generalization when training data does not represent real use [1].
- **Regularization and optimization:** Dropout randomly switches off units during training so that the network does not depend on any single unit [8]. Early stopping halts training when validation loss stops improving. Adam adapts the learning rate for each parameter and is widely used as a default optimizer [9].
- **Convolutional Neural Networks (CNN):** A 1D CNN slides filters over word embeddings and detects local patterns similar to n-grams, and has been shown to work well for sentence classification [7]. It trains quickly but sees only a limited window of text at a time.
- **Recurrent networks (RNN, LSTM, GRU):** An RNN processes words one at a time and passes a hidden state forward, but plain RNNs struggle to learn long-range dependencies. The LSTM adds gated memory cells to solve this [4], and the GRU is a lighter gated variant with fewer parameters [6]. A bidirectional RNN reads the sequence in both directions so that every position has context from before and after it [5].
- **Autoencoders and generative models:** Autoencoders learn compressed representations by reconstructing their input, and generative models such as GANs and large language models can produce realistic new text [1]. Generative models are relevant here because they can also be used to mass-produce convincing fake articles, which makes detection harder.
- **Transformers:** Pretrained transformer models such as BERT give strong contextual understanding of text [15] but are larger and slower to train, so they are left as future work.

### 2.2 Review of Related Works
- Early work on fake news detection used hand-crafted linguistic features and classical classifiers. Ahmed, Traore and Saad applied n-gram features with machine learning models to separate real and fake articles [11].
- Shu et al. surveyed the problem from a data-mining perspective, covering content-based, social-context and propagation-based approaches [12].
- Wang introduced the LIAR benchmark of short political statements labelled by factcheckers, which is widely used for evaluating generalization [13].
- Vosoughi, Roy and Aral studied the spread of true and false news on social media and reported that false stories reached people faster and more broadly than true ones, which shows why automated assistance is needed [14].
- Word embeddings such as GloVe provide pretrained word vectors that can initialize the embedding layer of a text model [10].
- Explainability methods such as LIME show which words influenced a prediction, which helps users trust and audit a classifier [16].

### 2.3 Comparative Study
| Approach | Strengths | Weaknesses | Suitability |
|---|---|---|---|
| **TF-IDF + Logistic Regression** | Fast, simple, interpretable | Ignores word order and context | Strong baseline |
| **1D CNN** | Captures local n-gram patterns, fast to train | Limited long-range context | Shorter texts |
| **LSTM / BiLSTM** | Models word order and long-range context | Slower sequential training | **Long articles (chosen)** |
| **GRU** | Fewer parameters than LSTM, often similar accuracy | Slightly simpler gating | Limited resources |
| **Transformer (BERT)** | Best contextual understanding, pretrained | Large, needs GPU | Future work |

#### Analysis:
- The BiLSTM suits long news articles because it reads the full sequence in both directions.
- Simpler models are cheaper but ignore word order, while transformers are more accurate but need far more compute.
- The BiLSTM gives a good balance of accuracy and computational cost for a course-level project on a CPU.

---

## CHAPTER 3: SYSTEM REQUIREMENTS & DESIGN

### 3.1 Hardware Requirements
- **Processor:** Intel i5 or higher
- **RAM:** Minimum 8 GB
- **Storage:** At least 2 GB free space (dataset and libraries)
- **GPU:** Optional (experiments ran on CPU-only cloud notebook runtime)
- **Operating System:** Windows / Linux / macOS, or a cloud notebook

### 3.2 Software Requirements
- **Programming language:** Python 3.x
- **Environment:** Jupyter Notebook, Google Colab or Kaggle Notebook
- **Libraries:** TensorFlow/Keras, NLTK, pandas, NumPy, scikit-learn, matplotlib
- **Dataset:** Kaggle “Fake and Real News” dataset (`Fake.csv` and `True.csv`)

### 3.3 System Architecture
The system follows an input–process–output architecture:
- **Input module:** Accepts article text (title and body).
- **Processing module:** Cleans text, converts it to padded integer sequences, and passes through embedding layer, BiLSTM, and dense layers.
- **Output module:** Displays the classification label (likely fake or likely real) along with fake probability.

### 3.4 Module Design
1. **Data Loading Module:** Reads CSV files, assigns labels (`fake = 1`, `real = 0`), merges title and body, and removes duplicate records.
2. **Preprocessing Module:** Performs lowercasing, removal of agency dateline, URLs, digits, punctuation, stopword removal, and lemmatization.
3. **Tokenization Module:** Builds 20,000-word vocabulary on training set and pads each article to 300 tokens.
4. **Model Module:** Embedding, BiLSTM, dropout, and dense classification layers.
5. **Training Module:** Adam optimizer, binary cross-entropy loss, early stopping on validation loss.
6. **Evaluation and Prediction Module:** Classification report, confusion matrix, training curves, and real-time prediction function.

### 3.5 Flowchart Description
```
Start 
  └──> Load Fake.csv and True.csv & Assign Labels (Fake=1, Real=0)
        └──> Merge Title + Body & Drop Duplicates
              └──> Clean & Normalize Text (Regex, Dateline Strip, Stopwords, Lemmatization)
                    └──> Stratified Train/Test Split (80% / 20%)
                          └──> Fit Keras Tokenizer (20k vocab) & Pad Sequences (maxlen=300)
                                └──> Build BiLSTM Model (Embedding -> BiLSTM -> Dropout -> Dense)
                                      └──> Train with Adam + EarlyStopping (patience=2)
                                            └──> Evaluate on Test Set (Precision, Recall, F1, Confusion Matrix)
                                                  └──> Predict On New Articles -> End
```

### 3.6 Model Architecture
| Layer | Output Shape | Parameters |
|---|---|---|
| **Embedding** (20,000 words, 128 dimensions) | `(None, 300, 128)` | 2,560,000 |
| **Bidirectional LSTM** (64 units each way) | `(None, 128)` | 98,816 |
| **Dropout (0.5)** | `(None, 128)` | 0 |
| **Dense (32 units, ReLU)** | `(None, 32)` | 4,128 |
| **Dropout (0.3)** | `(None, 32)` | 0 |
| **Dense (1 unit, Sigmoid)** | `(None, 1)` | 33 |
| **Total Parameters** | | **2,662,977** (approx. 10.7 MB) |

Most parameters reside in the embedding layer. The BiLSTM output has 128 values because it concatenates the forward and backward hidden states of 64 units each.

### 3.7 UML Diagrams
- **Use Case Diagram:**
  - Actor: User / Journalist / Fact-checker
  - Actions: Enter article text, run classification, view label and fake-probability, inspect token attributions.
- **Sequence Diagram:**
  1. User submits article text.
  2. Preprocessing module cleans, strips datelines, removes stopwords, lemmatizes, and tokenizes text.
  3. Model module computes forward pass through Embedding and BiLSTM layers.
  4. Output module displays verdict and calculated probabilities.

---

## CHAPTER 4: IMPLEMENTATION

### 4.1 Problem Definition
Given text $x$ of a news article (title and body), predict a label $y \in \{0, 1\}$, where:
- $y = 1 \implies$ **Fake**
- $y = 0 \implies$ **Real**

The model outputs probability $p = P(\text{fake} \mid x)$, and the article is classified as fake when $p > 0.5$.

### 4.2 Dataset Description
The project utilizes the Kaggle Fake and Real News Dataset containing two CSV files:
- `Fake.csv`: 23,481 articles flagged as fake or unreliable.
- `True.csv`: 21,417 articles collected from a legitimate news agency.

After merging, shuffling, label assignment, and duplicate removal, approximately **39,100 unique articles** remained. A stratified split of **80% train / 20% test** was performed, giving a test set of **7,821 articles** (4,239 real and 3,582 fake). 10% of the training portion (~3,100 articles) was held out for validation during training.

### 4.3 Data Leakage and Its Removal
Most real articles in this dataset begin with a news-agency dateline such as `"CITY (Reuters) -"`, which fake articles do not contain. A neural network can easily achieve near-100% training accuracy purely by memorizing this shortcut tag, learning zero semantic insight about deceptive language patterns. To ensure genuine evaluation, this prefix is stripped prior to training:
```python
text = re.sub(r"^.{0,60}\(reuters\)\s*-?\s*", "", text)
```
This directly addresses Course Outcome 1 (CO1) regarding practical issues in machine learning data hygiene.

### 4.4 Preprocessing Steps
| Step | Purpose |
|---|---|
| Lowercasing | Treat “News” and “news” as identical tokens |
| Remove agency dateline | Prevent label leakage and artifact bias |
| Remove URLs, digits, punctuation | Remove noise that carries little semantic meaning |
| Stopword & short-token removal | Drop frequent non-informative words (`"the"`, `"on"`, length $\le 2$) |
| Lemmatization (WordNet) | Reduce words to base lemma form (e.g., `"bills"` $\to$ `"bill"`) |

*Illustration:*  
`"WASHINGTON (Reuters) - The Senate voted on Tuesday on 3 bills, see http://example.com"`  
$\implies$ `"senate voted tuesday bill"`

### 4.5 Tokenization and Sequence Preparation
A Keras `Tokenizer` was fit **strictly on training articles** (to avoid test data leakage) with:
- `MAX_WORDS = 20,000`
- `oov_token = "<OOV>"`
- `MAX_LEN = 300` (post-padded and post-truncated)

### 4.6 Mathematical Formulations

#### LSTM Memory Cell Gates:
For input vector $x_t$ and previous hidden state $h_{t-1}$:
$$\begin{aligned}
f_t &= \sigma(W_f \cdot [h_{t-1}, x_t] + b_f) \quad &\text{(Forget Gate)} \\
i_t &= \sigma(W_i \cdot [h_{t-1}, x_t] + b_i) \quad &\text{(Input Gate)} \\
\tilde{c}_t &= \tanh(W_c \cdot [h_{t-1}, x_t] + b_c) \quad &\text{(Candidate State)} \\
c_t &= f_t \odot c_{t-1} + i_t \odot \tilde{c}_t \quad &\text{(Updated Cell State)} \\
o_t &= \sigma(W_o \cdot [h_{t-1}, x_t] + b_o) \quad &\text{(Output Gate)} \\
h_t &= o_t \odot \tanh(c_t) \quad &\text{(Hidden State)}
\end{aligned}$$

#### Bidirectional LSTM Output:
$$h_t^{\text{BiLSTM}} = [\overrightarrow{h_t} \,\|\, \overleftarrow{h_t}]$$

#### Loss Function (Binary Cross-Entropy):
$$\mathcal{L} = -\frac{1}{N} \sum_{i=1}^N \Big[ y_i \log \hat{y}_i + (1 - y_i) \log(1 - \hat{y}_i) \Big]$$

### 4.7 Regularization and Optimization (CO2)
| Technique | Setting | Purpose |
|---|---|---|
| **Dropout** | 0.5 after BiLSTM, 0.3 after Dense layer | Prevent co-adaptation of neurons and reduce overfitting |
| **Early Stopping** | Patience 2 on validation loss, restore best weights | Halt training before memorization occurs |
| **Adam Optimizer** | Learning rate $\eta = 0.001$, $\beta_1=0.9, \beta_2=0.999$ | Adaptive learning rates per parameter |
| **Mini-batch Training** | Batch size 64 | Efficient gradient computation and stable updates |
| **Validation Split** | 10% of training data (~3,100 articles) | Monitor out-of-sample generalization during training |

### 4.8 Pseudocode
```text
Algorithm FakeNewsBiLSTM(Fake.csv, True.csv):
Input: Two CSV files of labelled news articles
Output: Trained classifier and test-set metrics

1.  D <- merge(fake with label 1, real with label 0)
2.  remove duplicates from D
3.  for each article a in D:
4.      a <- clean(a)  // lowercase, remove dateline, URLs, digits, stopwords, lemmatize
5.  split D into train and test (80/20, stratified)
6.  fit tokenizer on train articles (20,000 words)
7.  X_train, X_test <- pad(tokenize(train), tokenize(test), length 300)
8.  build model: Embedding -> BiLSTM -> Dropout -> Dense -> Dropout -> Dense(sigmoid)
9.  repeat for up to 8 epochs:
10.     train one epoch with Adam and binary cross-entropy (batch 64)
11.     if validation loss has not improved for 2 epochs:
            stop, restore best weights
12. predictions <- (model(X_test) > 0.5)
13. report precision, recall, F1-score and confusion matrix
14. return model
```

### 4.9 Data Structures Used
- **Pandas DataFrame:** In-memory structured tabular storage for articles, labels, and cleaned texts.
- **Python Set:** $O(1)$ fast lookup for English stopword set.
- **Tokenizer Vocabulary Dictionary:** Maps word tokens to distinct integer IDs.
- **NumPy 2D Array ($N \times 300$):** Fixed-length padded integer sequences.
- **Weight Tensors:** Embedding matrix ($20,000 \times 128$) and recurrent weight matrices.

### 4.10 Sample Input & Output
- **Sample Input:**  
  `"Breaking: scientists confirm the moon is made of cheese"`
- **Sample Output:**  
  `LIKELY FAKE (fake-probability = 1.00)`

### 4.11 Complexity Analysis
- **Time Complexity:** For article of length $L$, single LSTM pass requires $\mathcal{O}(L \cdot h \cdot (d + h))$ operations ($h=64, d=128$). BiLSTM doubles this. Training took ~330 seconds per epoch on CPU. Prediction time for a single article requires just one forward pass ($< 15\text{ ms}$).
- **Space Complexity:** Model has 2,662,977 parameters $\approx 10.7\text{ MB}$ at 32-bit float precision.

---

## CHAPTER 5: RESULTS AND PERFORMANCE ANALYSIS

### 5.1 Experimental Setup
- **Hardware:** CPU-only cloud runtime
- **Configuration:** Batch size 64, Adam optimizer ($\text{lr}=0.001$), Early Stopping (patience=2)
- **Held-out Test Set:** 7,821 unseen articles (4,239 Real, 3,582 Fake)

### 5.2 Training Results per Epoch
| Epoch | Train Accuracy | Train Loss | Validation Accuracy | Validation Loss | Notes |
|---|---|---|---|---|---|
| 1 | 96.73% | 0.0873 | 99.30% | 0.0216 | Rapid convergence |
| **2** | **99.79%** | **0.0080** | **99.55%** | **0.0151** | **Best model checkpoint (restored)** |
| 3 | 99.95% | 0.0027 | 99.33% | 0.0265 | Val loss slightly rises |
| 4 | 99.93% | 0.0029 | 99.30% | 0.0245 | Early stopping triggered |

Validation loss reached its global minimum at **Epoch 2 (0.0151)**. Because validation loss did not improve in epochs 3 and 4, Early Stopping halted training and restored the optimal Epoch 2 weights.

### 5.3 Test Set Performance
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| **Real** | 0.99 | 0.99 | 0.99 | 4,239 |
| **Fake** | 0.99 | 0.99 | 0.99 | 3,582 |
| **Overall Accuracy** | | | **99.36%** | **7,821** |

#### Confusion Matrix:
| | Predicted Real | Predicted Fake | Total Actual |
|---|---|---|---|
| **Actual Real** | **4,214** (True Real) | 25 (False Fake) | 4,239 |
| **Actual Fake** | 25 (False Real) | **3,557** (True Fake) | 3,582 |

Out of 7,821 test articles, **7,771 were classified correctly**, with perfectly balanced errors (25 false positives and 25 false negatives).

### 5.4 Key Observations & Threats to Validity
- **Rapid Convergence:** The BiLSTM learns strong discriminative signals after a single epoch.
- **Dataset Bias:** A near-perfect score suggests stylized differences between real and fake corpora; real news primarily from a single news agency covering political issues in a defined time span.
- **Style vs. Truth:** The model evaluates linguistic and stylistic cues, not real-time fact-checking against ground truth databases.

---

## CHAPTER 6: CONCLUSION

This project designed, implemented, and thoroughly evaluated a Bidirectional LSTM classifier for automated fake news detection. Preprocessing pipelines eliminated data leakage from agency datelines, and early stopping with dropout regularization produced a stable, highly performant model reaching **99.36% test accuracy**.

### Learning Outcomes Achieved:
- **CO1:** Neural network architecture, overfitting, data leakage prevention.
- **CO2:** Regularization (dropout), optimization (Adam), early stopping.
- **CO3:** Comparative assessment of 1D CNNs vs RNNs for text.
- **CO4:** Recurrent sequence modeling with Bidirectional LSTM.
- **CO5:** Generative model threats and synthetic text detection challenges.

---

## CHAPTER 7: FUTURE ENHANCEMENTS

1. **Web Application:** Deployment of an interactive, responsive web user interface (React / Tailwind / FastAPI) allowing real-time pasting, URL scraping, and probability visualization.
2. **Pretrained Transformers:** Fine-tuning BERT, RoBERTa, or DeBERTa for richer semantic representations.
3. **Hybrid Architectures:** CNN-LSTM hybrids combining local n-gram extraction with recurrent sequence dependencies.
4. **Explainability & Attribution:** Integrating LIME / SHAP / attention heatmaps for token-level explainability.
5. **Multimodal Verification:** Extending detection to cover images, deepfakes, and cross-platform viral claims.

---

## CHAPTER 8: REFERENCES

### 8.1 Textbooks
- [1] Goodfellow, I., Bengio, Y., and Courville, A. (2016). *Deep Learning*. MIT Press.
- [2] Aggarwal, C. C. (2018). *Neural Networks and Deep Learning*. Springer.
- [3] Chollet, F. (2021). *Deep Learning with Python* (2nd ed.). Manning Publications.

### 8.2 Research Papers
- [4] Hochreiter, S. and Schmidhuber, J. (1997). Long short-term memory. *Neural Computation*, 9(8), 1735–1780.
- [5] Schuster, M. and Paliwal, K. K. (1997). Bidirectional recurrent neural networks. *IEEE Transactions on Signal Processing*, 45(11), 2673–2681.
- [6] Cho, K., et al. (2014). Learning phrase representations using RNN encoder–decoder for statistical machine translation. *EMNLP 2014*.
- [7] Kim, Y. (2014). Convolutional neural networks for sentence classification. *EMNLP 2014*.
- [8] Srivastava, N., et al. (2014). Dropout: A simple way to prevent neural networks from overfitting. *JMLR*, 15(1), 1929–1958.
- [9] Kingma, D. P. and Ba, J. (2015). Adam: A method for stochastic optimization. *ICLR 2015*.
- [10] Pennington, J., Socher, R., and Manning, C. (2014). GloVe: Global vectors for word representation. *EMNLP 2014*.
- [11] Ahmed, H., Traore, I., and Saad, S. (2017). Detection of online fake news using n-gram analysis and machine learning techniques. *ISDDC 2017*.
- [12] Shu, K., Sliva, A., Wang, S., Tang, J., and Liu, H. (2017). Fake news detection on social media: A data mining perspective. *ACM SIGKDD*, 19(1), 22–36.
- [13] Wang, W. Y. (2017). “Liar, liar pants on fire”: A new benchmark dataset for fake news detection. *ACL 2017*.
- [14] Vosoughi, S., Roy, D., and Aral, S. (2018). The spread of true and false news online. *Science*, 359(6380), 1146–1151.
- [15] Devlin, J., et al. (2019). BERT: Pre-training of deep bidirectional transformers for language understanding. *NAACL 2019*.
- [16] Ribeiro, M. T., Singh, S., and Guestrin, C. (2016). “Why should I trust you?”: Explaining the predictions of any classifier. *KDD 2016*.

### 8.3 Online Resources & Syllabus
- [17] Bisaillon, C. *Fake and Real News Dataset*. Kaggle.
- [18] TensorFlow and Keras Documentation.
- [19] NLTK Documentation.
- [20] APJ Abdul Kalam Technological University. *AIT-401 Foundations of Deep Learning Syllabus*.

---

## APPENDIX A: SOURCE CODE

```python
"""
Complete Python implementation (fake_news_lstm.py)
Requirements: pip install pandas numpy scikit-learn nltk tensorflow matplotlib
"""

import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Bidirectional, LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping

nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)

MAX_WORDS = 20000  # vocabulary size
MAX_LEN = 300      # tokens kept per article
EMBED_DIM = 128

# ---------------------------------------------------------------- 1. Load
fake = pd.read_csv("Fake.csv")
fake["label"] = 1  # 1 = fake
real = pd.read_csv("True.csv")
real["label"] = 0  # 0 = real
df = pd.concat([fake, real], ignore_index=True).sample(frac=1, random_state=42)
df["text_raw"] = df["title"].fillna("") + " " + df["text"].fillna("")
df = df.drop_duplicates(subset="text_raw")

# ------------------------------------------------------- 2. Preprocessing
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

def clean(text: str) -> str:
    text = text.lower()
    # Remove dataset artifacts that leak the label (real articles start with "CITY (Reuters) -")
    text = re.sub(r"^.{0,60}\(reuters\)\s*-?\s*", "", text)
    text = re.sub(r"http\S+|www\.\S+", " ", text)  # URLs
    text = re.sub(r"[^a-z\s]", " ", text)          # punctuation / digits
    tokens = [
        lemmatizer.lemmatize(w)
        for w in text.split()
        if w not in stop_words and len(w) > 2
    ]
    return " ".join(tokens)

df["clean"] = df["text_raw"].apply(clean)

# ----------------------------------------------- 3. Tokenize + pad + split
X_train_txt, X_test_txt, y_train, y_test = train_test_split(
    df["clean"], df["label"], test_size=0.2, stratify=df["label"], random_state=42
)

tokenizer = Tokenizer(num_words=MAX_WORDS, oov_token="<OOV>")
tokenizer.fit_on_texts(X_train_txt)  # fit on train only (no leakage)

def to_seq(texts):
    return pad_sequences(
        tokenizer.texts_to_sequences(texts),
        maxlen=MAX_LEN,
        padding="post",
        truncating="post"
    )

X_train, X_test = to_seq(X_train_txt), to_seq(X_test_txt)
y_train, y_test = np.array(y_train), np.array(y_test)

# ------------------------------------------------------------- 4. Model
model = Sequential([
    Embedding(MAX_WORDS, EMBED_DIM),
    Bidirectional(LSTM(64, return_sequences=False)),
    Dropout(0.5),
    Dense(32, activation="relu"),
    Dropout(0.3),
    Dense(1, activation="sigmoid"),
])

model.compile(
    loss="binary_crossentropy",
    optimizer="adam",
    metrics=["accuracy"]
)
model.summary()

history = model.fit(
    X_train,
    y_train,
    validation_split=0.1,
    epochs=8,
    batch_size=64,
    callbacks=[EarlyStopping(patience=2, restore_best_weights=True)]
)

# ----------------------------------------------------------- 5. Evaluate
probs = model.predict(X_test).ravel()
preds = (probs > 0.5).astype(int)

print(classification_report(y_test, preds, target_names=["Real", "Fake"]))
print("Confusion matrix:\n", confusion_matrix(y_test, preds))

plt.plot(history.history["accuracy"], label="train")
plt.plot(history.history["val_accuracy"], label="val")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.legend()
plt.title("BiLSTM training curve")
plt.savefig("training_curve.png", dpi=150)

# ------------------------------------------------------------ 6. Predict
def predict_article(text: str) -> str:
    p = model.predict(to_seq([clean(text)]), verbose=0)[0][0]
    label = "LIKELY FAKE" if p > 0.5 else "LIKELY REAL"
    return f"{label} (fake-probability = {p:.2f})"

if __name__ == "__main__":
    print(predict_article("Breaking: scientists confirm the moon is made of cheese"))
    model.save("fake_news_bilstm.keras")
```
