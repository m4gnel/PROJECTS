// Project metadata, academic training curves, and confusion matrix data
// from the AIT-401 Foundations of Deep Learning Course Project Report

export const PROJECT_METADATA = {
  title: 'Fake News Detection using LSTM',
  course: 'AIT-401 – Foundations of Deep Learning',
  institution: 'Adi Shankara Institute of Engineering and Technology, Kalady',
  university: 'APJ Abdul Kalam Technological University (KTU), Kerala',
  department: 'Department of AI and DS',
  academicYear: '2026–27',
  date: 'October 2026',
  authors: [
    { name: 'Krishna Priya V R', roll: 'ASI23CA039' },
    { name: 'Magnel Olivero', roll: 'ASI23CA040' },
    { name: 'Miliya Rose Sephy', roll: 'ASI23CA041' }
  ],
  guide: 'Prof. Asha Rose Thomas',
  hod: 'Dr. Sarika S',
  overallAccuracy: 99.36,
  testArticlesCount: 7821,
  totalParameters: 2662977,
  modelSizeMB: 10.7
};

export const TRAINING_EPOCHS = [
  { epoch: 1, trainAcc: 96.73, trainLoss: 0.0873, valAcc: 99.30, valLoss: 0.0216, note: 'Initial rapid convergence' },
  { epoch: 2, trainAcc: 99.79, trainLoss: 0.0080, valAcc: 99.55, valLoss: 0.0151, note: 'Optimal checkpoint (lowest val loss restored)' },
  { epoch: 3, trainAcc: 99.95, trainLoss: 0.0027, valAcc: 99.33, valLoss: 0.0265, note: 'Slight val loss increase' },
  { epoch: 4, trainAcc: 99.93, trainLoss: 0.0029, valAcc: 99.30, valLoss: 0.0245, note: 'EarlyStopping triggered (patience=2)' }
];

export const CONFUSION_MATRIX = {
  trueReal: 4214,
  falseFake: 25,
  falseReal: 25,
  trueFake: 3557,
  totalTest: 7821,
  totalCorrect: 7771,
  accuracy: 99.36
};

export const CLASSIFICATION_REPORT = [
  { class: 'Real News', precision: 0.99, recall: 0.99, f1: 0.99, support: 4239 },
  { class: 'Fake News', precision: 0.99, recall: 0.99, f1: 0.99, support: 3582 },
  { class: 'Macro Avg', precision: 0.99, recall: 0.99, f1: 0.99, support: 7821 },
  { class: 'Weighted Avg', precision: 0.99, recall: 0.99, f1: 0.99, support: 7821 }
];

export const ARCHITECTURE_LAYERS = [
  {
    layerName: 'Embedding Layer',
    outputShape: '(None, 300, 128)',
    params: '2,560,000',
    description: 'Maps 20,000 unique word IDs to dense 128-dimensional learned feature vectors.'
  },
  {
    layerName: 'Bidirectional LSTM',
    outputShape: '(None, 128)',
    params: '98,816',
    description: 'Two LSTM recurrent layers (64 units forward + 64 units backward) reading sequence bidirectionally.'
  },
  {
    layerName: 'Dropout (0.5)',
    outputShape: '(None, 128)',
    params: '0',
    description: 'Randomly drops 50% of recurrent feature activations during training to prevent co-adaptation.'
  },
  {
    layerName: 'Dense (ReLU)',
    outputShape: '(None, 32)',
    params: '4,128',
    description: 'Fully connected 32-unit layer with Rectified Linear Unit activation for non-linear representation.'
  },
  {
    layerName: 'Dropout (0.3)',
    outputShape: '(None, 32)',
    params: '0',
    description: 'Secondary regularization layer dropping 30% of connections before the output unit.'
  },
  {
    layerName: 'Dense (Sigmoid)',
    outputShape: '(None, 1)',
    params: '33',
    description: 'Single output unit with sigmoid activation computing fake probability p = P(fake | x).'
  }
];

export const AVAILABLE_MODELS = [
  {
    id: 'bilstm-optimal',
    name: 'BiLSTM Neural Net (99.36% Acc)',
    badge: 'Production Checkpoint',
    desc: 'Trained on 39,100 Kaggle articles with WordNet lemmatization & dateline filtering',
    iconColor: '#f59e0b'
  },
  {
    id: 'claude-sonnet',
    name: 'Claude-3.5-sonnet',
    badge: 'LLM Multi-Modal',
    desc: 'Deep linguistic reasoning & context analysis (matches prompt mockup)',
    iconColor: '#f97316'
  },
  {
    id: 'bilstm-glove',
    name: 'BiLSTM + GloVe Vectors (100d)',
    badge: 'Pretrained Embeddings',
    desc: 'Enhanced with pre-trained GloVe representations for out-of-domain robustness',
    iconColor: '#8b5cf6'
  },
  {
    id: 'tfidf-baseline',
    name: 'TF-IDF + Logistic Regression',
    badge: 'Linear Baseline',
    desc: 'Traditional machine learning baseline reviewed in Chapter 2',
    iconColor: '#06b6d4'
  }
];

export const INITIAL_PROJECTS = [
  { id: 'pirnjo', name: 'Pirnjo', count: '03', category: 'Breaking News' },
  { id: 'meku', name: 'Meku', count: '02', category: 'Political Claims' },
  { id: 'formbold', name: 'Formbold', count: '04', category: 'Social Media Viral' },
  { id: 'tailadmin', name: 'Tailadmin', count: '03', category: 'Health & Science' }
];
