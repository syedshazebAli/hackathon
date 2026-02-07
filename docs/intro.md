---
id: intro
title: Physical AI & Humanoid Robotics
hide_title: false
sidebar_label: Overview
slug: /intro
keywords:
  - Physical AI
  - Humanoid Robotics
  - Sensors
  - Perception
  - Cognition
---

import {Insight, Engineering, AILogic, Divider} from '@site/src/components/Callouts.mdx';

# Physical AI & Humanoid Robotics

This textbook introduces Physical AI and Humanoid Robotics in a simple, structured way. Physical AI refers to artificial intelligence systems that can sense, think, and act in the real world.

<Insight>
Physical AI links embodied sensing/actuation with cognition. It is not purely software; it is a closed loop between the world and the controller.
</Insight>

This course is designed for beginners, students, and hackathon participants. No advanced mathematics is required.

<Divider />

## What you will learn

- System architecture across perception, control, and cognition
- Sensor and actuator fundamentals for humanoid robots
- Software stack design patterns and safety practices

<Engineering>
Favor composable modules with clear data contracts between perception, control, and planning. Start from deterministic control, then layer learned components.
</Engineering>

<AILogic>
Use task graphs and behavior trees to structure complex action policies. Couple them with state estimators for robust execution.
</AILogic>