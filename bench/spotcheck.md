# Spot-check: 20 papers

For each paper, write 2 (fits the facet: same problem AND same or closely related method), 1 (partly), or 0 (does not fit).
Judge only from the text shown. Do not look up the paper. Fill in your label after `Your label:`.

## 1. Real-time Hand Gesture Detection and Classification Using Convolutional Neural Networks

Facet: CNN face detection with YuNet (task: face detection; method: lightweight anchor-free CNN detector (YuNet) via ONNX; setting: real-time, CPU, webcam frames)

> Real-time recognition of dynamic hand gestures from video streams is a challenging task since (i) there is no indication when a gesture starts and ends in the video, (ii) performed gestures should only be recognized once, and (iii) the entire architecture should be designed considering the memory and power budget. In this work, we address these challenges by proposing a hierarchical structure enabling offline-working convolutional neural network (CNN) architectures to operate online efficiently by using sliding window approach. The proposed architecture consists of two models: (1) A detector w...

Your label: 

## 2. Automating Attendance Management in Human Resources: A Design Science Approach Using Computer Vision and Facial Recognition

Facet: Haar cascade face detection (task: face detection; method: boosted cascade of Haar-like features (Viola-Jones); setting: real-time, CPU)

> Haar Cascade is a cost-effective and user-friendly machine learning-based algorithm for detecting objects in images and videos. Unlike Deep Learning algorithms, which typically require significant resources and expensive computing costs, it uses simple image processing techniques like edge detection and Haar features that are easy to comprehend and implement. By combining Haar Cascade with OpenCV2 on an embedded computer like the NVIDIA Jetson Nano, this system can accurately detect and match faces in a database for attendance tracking. This system aims to achieve several specific objectives t...

Your label: 

## 3. Thai named entity recognition based on conditional random fields

Facet: Thai named entity recognition (task: named entity recognition; method: conditional random fields (PyThaiNLP thainer); setting: Thai language)

> This paper presents the Thai named entity recognition (NER) systems using Conditional Random Fields (CRFs). In the previous studies of Thai NER, there are not any systems using syllable-segmented data as an input but word-segmented one. Since the results of some researches on NER in other languages such as Chinese show that the systems based on character are better than those based on word, this study is also conducted to find out if the syllable-segmented input helps improve Thai NER. In order to compare the system getting word-segmented input to that getting syllable-segmented input, there w...

Your label: 

## 4. NER2Map: Positive Transfer from Named Entity Recognition to Address Parsing in Low Data Regimes

Facet: Thai address parsing (task: parsing free-text postal addresses into fields; method: rule-based parsing with gazetteer lookup; setting: Thai language, noisy chat text)

> In natural language processing, the time and human resource costs associated with data labeling have led to a focus on solving problems with limited data. In this study, two separate models for Address Parsing were developed using transfer lear-ning methods. Specifically, the BERT model was first fine-tuned on the NER dataset, and then the effects of fine-tuning on a relatively small Address Parsing dataset were examined, resulting in a method called NER2Map. Experimental results show that the NER2Map model achieves higher accuracy in predicting correct labels with limited data compared to dir...

Your label: 

## 5. Face detection using SURF cascade

Facet: Haar cascade face detection (task: face detection; method: boosted cascade of Haar-like features (Viola-Jones); setting: real-time, CPU)

> We present a novel boosting cascade based face detection framework using SURF features. The framework is derived from the well-known Viola-Jones (VJ) framework but distinguished by two key contributions. First, the proposed framework deals with only several hundreds of multidimensional local SURF patches instead of hundreds of thousands of single dimensional haar features in the VJ framework. Second, it takes AUC as a single criterion for the convergence test of each cascade stage rather than the two conflicting criteria (false-positive-rate and detection-rate) in the VJ framework. These modif...

Your label: 

## 6. Novel AI Camera Camouflage: Face Cloaking Without Full Disguise

Facet: Haar cascade face detection (task: face detection; method: boosted cascade of Haar-like features (Viola-Jones); setting: real-time, CPU)

> This study demonstrates a novel approach to facial camouflage that combines targeted cosmetic perturbations and alpha transparency layer manipulation to evade modern facial recognition systems. Unlike previous methods -- such as CV dazzle, adversarial patches, and theatrical disguises -- this work achieves effective obfuscation through subtle modifications to key-point regions, particularly the brow, nose bridge, and jawline. Empirical testing with Haar cascade classifiers and commercial systems like BetaFaceAPI and Microsoft Bing Visual Search reveals that vertical perturbations near dense fa...

Your label: 

## 7. A Cascade of Boosted Generative and Discriminative Classifiers for Vehicle Detection

Facet: Haar cascade face detection (task: face detection; method: boosted cascade of Haar-like features (Viola-Jones); setting: real-time, CPU)

> We present an algorithm for the on-board vision vehicle detection problem using a cascade of boosted classifiers. Three families of features are compared: the rectangular filters (Haar-like features), the histograms of oriented gradient (HoG), and their combination (a concatenation of the two preceding features). A comparative study of the results of the generative (HoG features), discriminative (Haar-like features) detectors, and of their fusion is presented. These results show that the fusion combines the advantages of the other two detectors: generative classifiers eliminate "easily" negati...

Your label: 

## 8. PROPER FACE MASK DETECTION USING HAAR CASCADE

Facet: Haar cascade face detection (task: face detection; method: boosted cascade of Haar-like features (Viola-Jones); setting: real-time, CPU)

> This project was created to detect the use of masks, where the use of masks is now the obligation of all communities, especially in public places. In this project, we will detect people who don't care and are not wearing masks properly. In detecting the use of masks, the Haar Cascade algorithm is used to detect facial, eye, nose, and mouth objects. There are 3 libraries to help detect masks such as haarcascade_frontalface_default.xml to detect face objects from the front side, haarcascade_eye.xml to detect eye objects, Nariz.xml to detect nose objects, and haarcascade_mcs_mouth.xml to detect m...

Your label: 

## 9. Thai Named Entity Recognition Using BiLSTM-CNN-CRF Enhanced by TCC

Facet: Thai named entity recognition (task: named entity recognition; method: conditional random fields (PyThaiNLP thainer); setting: Thai language)

> The languages spoken in Asia share common morphological analysis errors in word segmentation which normally propagate to higher-level processing, i.e., POS tagging, syntactic parsing, word extraction, and NER, as we discuss in this research. We introduce the Thai character cluster (TCC) to reduce the errors propagated from word segmentation and POS tagging by incorporating into character representation layer of BiLSTM for NER. The initial NER model is created from the original THAI-NEST named-entity tagged corpus by applying the best performing BiLSTM-CNN-CRF model with word, part-of-speech, a...

Your label: 

## 10. A Conditional Random Field Approach for Named Entity Recognition in Bengali and Hindi

Facet: Thai named entity recognition (task: named entity recognition; method: conditional random fields (PyThaiNLP thainer); setting: Thai language)

> This paper describes the development of Named Entity Recognition (NER) systems for two leading Indian languages, namely Bengali and Hindi, using the Conditional Random Field (CRF) framework. The system makes use of different types of contextual information along with a variety of features that are helpful in predicting the different named entity (NE) classes. This set of features includes language independent as well as language dependent components. We have used the annotated corpora of 122,467 tokens for Bengali and 502,974 tokens for Hindi tagged with a tag set of twelve different NE classe...

Your label: 

## 11. Unsupervised face analysis from multi-view

Facet: Haar cascade face detection (task: face detection; method: boosted cascade of Haar-like features (Viola-Jones); setting: real-time, CPU)

> Face detection, localization and recognition from multi-poses are one of the most challenging topics in the area of computer vision and pattern recognition. During the past decade several methods have been proposed for face detection and recognition but they mainly concentrate on frontal faces. Although in recent years, some methods have been proposed based on sliding windows to exhaustively search through the image in many scales and views, they are slow and their performance on multi-view or multi-pose faces are not as good as frontal face detections. Training these methods is also a bottlen...

Your label: 

## 12. Comprehensive Benchmarking and Analysis of Open Pretrained Thai Speech Recognition Models

Facet: Thai named entity recognition (task: named entity recognition; method: conditional random fields (PyThaiNLP thainer); setting: Thai language)

> This paper presents a comprehensive benchmarking and analysis of open pretrained Thai Automatic Speech Recognition (ASR) models, addressing a critical gap in low-resource language ASR development. Our benchmarking focuses on one foundation speech model, three Open Thai Speech Recognition Models, and Open speech APls. We evaluate these models, including our fine-tuned Whisper model, across diverse speech types and acoustic environments. The study reveals significant performance gaps between read and spontaneous speech, with models performing well in controlled settings but struggling in real-wo...

Your label: 

## 13. Geo-referencing Place from Everyday Natural Language Descriptions

Facet: Fuzzy matching for typo correction (task: correcting misspelled place names against a gazetteer; method: edit-distance fuzzy string matching (RapidFuzz ratio); setting: short strings, Thai place names)

> Natural language place descriptions in everyday communication provide a rich source of spatial knowledge about places. An important step to utilize such knowledge in information systems is geo-referencing all the places referred to in these descriptions. Current techniques for geo-referencing places from text documents are using place name recognition and disambiguation; however, place descriptions often contain place references that are not known by gazetteers, or that are expressed in other, more flexible ways. Hence, the approach for geo-referencing presented in this paper starts from a pla...

Your label: 

## 14. Deteksi Citra Wajah Menggunakan Algoritma Haar Cascade Classifier

Facet: Haar cascade face detection (task: face detection; method: boosted cascade of Haar-like features (Viola-Jones); setting: real-time, CPU)

> Manusia dapat mengenali objek dengan sangat mudah berbeda dengan komputer. Jika komputer ingin mengenali sebuah objek harus dilakukan proses pelatihan yang sangat lama ada banyak sekali metode yang dapat digunakan untuk melatih komputer agar dapat mendeteksi suatu objek dengan baik salah satunya yaitu dengan algoritma haar cascade classifier. Pada penelitian ini akan membawakan topik pendeteksian wajah yang akan dilakukan dengan menggunakan algoritma haar cascade classifier. Algoritma haar cascade classifier sudah menjadi algoritma yang biasa digunakan untuk pendeteksian wajah. Dengan mengguna...

Your label: 

## 15. Top2Vec: Distributed Representations of Topics

Facet: Thai named entity recognition (task: named entity recognition; method: conditional random fields (PyThaiNLP thainer); setting: Thai language)

> Topic modeling is used for discovering latent semantic structure, usually referred to as topics, in a large collection of documents. The most widely used methods are Latent Dirichlet Allocation and Probabilistic Latent Semantic Analysis. Despite their popularity they have several weaknesses. In order to achieve optimal results they often require the number of topics to be known, custom stop-word lists, stemming, and lemmatization. Additionally these methods rely on bag-of-words representation of documents which ignore the ordering and semantics of words. Distributed representations of document...

Your label: 

## 16. Conditional Random Fields for Biomedical Named Entity Recognition Revisited

Facet: Thai named entity recognition (task: named entity recognition; method: conditional random fields (PyThaiNLP thainer); setting: Thai language)

> Abstract Named Entity Recognition (NER) is a key task which automatically extracts Named Entities (NE) from the text. Names of persons, places, date and time are examples of NEs. We are applying Conditional Random Fields (CRFs) for NER in biomedical domain. Examples of NEs in biomedical texts are gene, proteins. We used a minimal set of features to train CRF algorithm and obtained a good results for biomedical texts.

Your label: 

## 17. Face Detection Using Haar Cascade Algorithm

Facet: Haar cascade face detection (task: face detection; method: boosted cascade of Haar-like features (Viola-Jones); setting: real-time, CPU)

> Nowadays, machines are becoming friendlier and can react to people in a faster way. Human face detection has attractive wide spread interest in recent years and become a vital factor in Human Machine Interaction and one of the most popular topics in computer vision and biometrics. The aim of this paper is to detect human face from an image containing simple and complex backgrounds using the Haar cascade algorithm. The three principal of this algorithm are: Haar-like Filter, Integral Image and the AdaBoost cascade classifier. The available Labeled Faces in the Wild (LFW) is used as the research...

Your label: 

## 18. ASMNet: a Lightweight Deep Neural Network for Face Alignment and Pose Estimation

Facet: CNN face detection with YuNet (task: face detection; method: lightweight anchor-free CNN detector (YuNet) via ONNX; setting: real-time, CPU, webcam frames)

> Active Shape Model (ASM) is a statistical model of object shapes that represents a target structure. ASM can guide machine learning algorithms to fit a set of points representing an object (e.g., face) onto an image. This paper presents a lightweight Convolutional Neural Network (CNN) architecture with a loss function being assisted by ASM for face alignment and estimating head pose in the wild. We use ASM to first guide the network towards learning a smoother distribution of the facial landmark points. Inspired by transfer learning, during the training process, we gradually harden the regress...

Your label: 

## 19. Geographic Ontologies, Gazetteers and Multilingualism

Facet: Fuzzy matching for typo correction (task: correcting misspelled place names against a gazetteer; method: edit-distance fuzzy string matching (RapidFuzz ratio); setting: short strings, Thai place names)

> Different languages imply different visions of space, so that terminologies are different in geographic ontologies. In addition to their geometric shapes, geographic features have names, sometimes different in diverse languages. In addition, the role of gazetteers, as dictionaries of place names (toponyms), is to maintain relations between place names and location. The scope of geographic information retrieval is to search for geographic information not against a database, but against the whole Internet: but the Internet stores information in different languages, and it is of paramount importa...

Your label: 

## 20. Thai Named Entity Recognition Using Bi-LSTM-CRF with Word and Character Representation

Facet: Thai named entity recognition (task: named entity recognition; method: conditional random fields (PyThaiNLP thainer); setting: Thai language)

> Named Entity Recognition (NER) is a handy tool for many natural language processing tasks to identify and extract a unique entity such as person, location, organization and time. In English and Chinese, NER has been thoroughly researched and is able to be applied in more practical settings. Its development in Thai is still limited because of rare resources and language difficulties such as the lack of boundary indicator for words, phrases and sentences. In this paper, we present an application of Bi-LSTM-CRF with word/character level representation, to solve this problem. Firstly, we prepared ...

Your label: 
