---
slug: nodysseus-three-live-lowcoding-three-js-visuals-in-the-browser
status: proof
title: 'Nodysseus.THREE: Live Lowcoding THREE.js Visuals in the Browser'
type: workshop
submission_type: Workshop
contributors:
- person: $popple-ulysses
---

# $PROGRAM_NOTE

Using Nodysseus, a node-editor for the browser, we'll explore creating and using reusable node networks with 3D objects. This is a hands on tutorial quite literally - participants can use their touch device of choice or their laptops, it works well on both. By the end of the workshop, participants will be more comfortable thinking in node networks and have a spiffy live(low)code party trick they can revisit at any time.

# $ABSTRACT

Our interactions with computers have evolved drastically over the last few years. A significant portion of the world interact with two or more devices daily, but the tools for programming these devices have stayed largely the same since inception. Most programmers use a keyboard and mouse primarily, and only a small portion of end users know how to program their devices. Nodysseus is a visual programming language and editor which aims to bridge the device divide and provide all users an easy way to program from their web browser. 

Nodysseus follows in the footsteps of well established node-based editors such as Pure Data, Houdini, Max MSP, TouchDesigner, Unity, and Unreal. Some of these editors are used within the livecode community for their approachability and visual feedback. Others are used in the games and visual effects world to provide artists with a simple interface for putting together complex systems. In both cases, the visual feedback and easy logic-reuse enable quick iteration and open creative pathways that might be more difficult to navigate using a traditional text-based editor. 

All of the editors mentioned are primarily siloed desktop applications, whereas Nodysseus utilizes modern Javascript to offer a similar in-browser experience from any device. There is no download step, and by default all created data is stored locally for offline use and privacy. Users can also connect to each other over webrtc for collaboration through real-time graph updates. It offers artists and coders of all disciplines a playground for trying out new ideas then packaging and easily sharing them, no matter which device they have access to or how technical they might consider themselves. 

In the first part of this workshop, we'll create a basic reusable graph with Nodysseus and THREE.js that rotates some input geometry in time with a beat. Participants will be able to follow along from any device. Starting from a THREE.js example graph, we'll create nodes that rotate a cube, and package the nodes up into a reusable graph. Then we'll add a slider to the graph to change the speed of the rotation, and use a prebuilt "tap beat" node before the graph to make it move to a beat. We'll export our rotation graph as a .json for sharing and future use. 

The second part of the workshop will be more freeform - participants will either stay with the graph from the first part or explore a more complex pre-built node that moves objects according to curl noise. The curl noise example will have multiple different input parameters that can be replaced with sliders, tap buttons, timing functions, materials, etc. In this part of the workshop, participants will have the opportunity to receive one-on-one instruction to come to grasps with the system as a whole. 

By the end of the workshop, participants will be comfortable creating reusable components in Nodysseus and exporting them or sharing them through a connection. Hopefully this will open up new avenues of collaboration and allow them more opportunities to explore creative ideas on the go.
