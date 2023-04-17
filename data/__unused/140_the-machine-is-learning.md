---
slug: the-machine-is-learning
status: proof
title: the machine is learning
type: performance
submission_type: Performance
contributors:
- person: $baalman-marije
---

# $PROGRAM_NOTE

The performance *the machine is learning* is a theatrical performance
highlighting the process of training a machine with realtime gestures: the
labour that is absent from most dialogues on machine learning. In an
attempt to livecode with gestures, the performer finds herself directed by
the machine to repetitively make gestures to generate time series data
samples for the machine to learn from.

While the popular discussion and criticism of AI tends to focus on issues of
privacy, the use of AI in decision making and possible job loss, the labour
involved in making machine learning algorithms work is less prominent. The
labour involved in AI consists not only of designing and programming
algorithms, but also in generating and categorising these data samples. The
working conditions of these tasks are generally not known.

# $ABSTRACT

*the machine is learning* is a performance developed in the context of
creating a gestural live coding language: GeCoLa. The key concept of this
coding language is that the code is written by gestures, rather than by
written text based language. Gestures are defined for keywords/operations
in the language and variable names are defined as gestures learned on the
fly. Seemingly a simple approach, just use some machine learning algorithm
to detect the gestures and have detected gestures evoke keywords and
variable names. But it is not that simple. Time-based gestures (rather than
instantaneous poses) are not easily learned by a machine and certainly not
when they are not predefined and linked to a large database of templates of
said gesture. The teaching of the machine is a lengthy process and requires
a human to repeatedly make a gesture so the machine can learn to
recognise the gesture and accurate labeling of type, start and end of
gesture. The performance the machine is learning focuses on this process
and the dialog of the human with the machine to record and train the
machine, so that it can then recognise the gestures. The training of
machines and the hidden labour of humans involved in generating, labeling
and validating the data fed into machine learning algorithms is a topic that
is often missing from (critical) dialogues about machine learning, even when
awareness about assumptions in algorithms and data bias is rising.

More information on the coding language can be found here:

<https://marijebaalman.eu/projects/gecola.html>

In the performance the [Sense/Stage MiniBee](https://sensestage.eu/) is used as a wireless sensing
platform along with a 9 d.o.f.-sensor, an LSM9DS1, and a button interface
used previously in the performance Wezen-Gewording.

The gesture recognition algorithm is implemented using the [Gesture
Recognition Toolkit](http://www.nickgillian.com/wiki/pmwiki.php/GRT/GestureRecognitionToolkit) by Nick Gillian.
