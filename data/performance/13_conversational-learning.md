---
slug: conversational-learning
title: Conversational Learning
type: performance
submission_type: Performance
contributors:
- person: $paz-ivan
---

# $PROGRAM_NOTE

Conversational learning explores live coding liveness within the machine learning process (data collection, training and validation), focusing on how real-time training of a machine learning algorithm can be sonically exposed. It is based on a rule-learning algorithm that automatically produces new synthesizer presets out of a small labeled database. The algorithm is designed with only two parameters controlling “how close” the new created presets can be from those originally present in the training data. The learning process happens mid-performance, tweaking the algorithm parameters on-the-fly. Then, the different learned models unfold the piece in conversation with the performer.

# $ABSTRACT

Conversational learning explores live coding liveness within the machine learning process (data collection, training and validation), focusing on how the real-time training of a machine learning algorithm can be sonically exposed. It is based on a rule-learning algorithm that automatically produces new synthesizer presets out of a small labeled database. The algorithm is designed with only two parameters (I did that on purpose) controlling “how close” the new created presets can be from those originally present in the training data. The learning process happens mid-performance, tweaking the algorithm parameters on-the-fly. Then, the different learned models unfold the piece in conversation with the performer. For example, it is possible to have a model that replicates the training data or to extract 700 -to say a number- new variations with the risk of having unpleasant surprises. The performance starts form scratch and the data labels are used to conduct the sections and the sound moments of the performance. The sound synthesis is carried out in SuperCollider and the syntax looks like: ruler data.csv distance:4 consistency:0.5 ~set.value(Ndef(\x),~rules,‘r’,‘rain’) In the first function - ruler - is the algorithm (stands for rule learning) data.csv is the training dataset, distance and consistency together control the induction process. In the second function (around minute 2:29 of the video) we specify the Synth, the rules form which the new preset is taken the number of preset (in case we want) and the label or class. For this performance I will focus on training different models mid-performance (I normally train some models but this have not been the main focus). Unfortunately I do not have a better version of a performance with the current system. The submitted link is a mocked up of the last performance (past July). The code is not specially visible but the different moments of the performance are well illustrated.