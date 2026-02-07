
# Chapter 6: Learning in Physical Systems

A pre-programmed robot can follow fixed rules—but a **learning robot** can **adapt, improve, and handle the unexpected**.  
In Physical AI, learning doesn’t happen just in simulation; it happens **through real interaction with the physical world**.

This ability to learn from doing—just like humans—is what makes robots truly intelligent and useful in changing environments.

## How Do Robots Learn?

Unlike humans, robots learn through structured AI methods. Here are the three most common approaches used in humanoid robotics:

### 1. 📚 Supervised Learning  
- The robot learns from **labeled examples**.  
- Example: Show 10,000 images of “cup” vs. “bottle,” and train a vision model to tell them apart.  
- **Use case**: Object recognition, speech-to-text, gesture classification.

> ✅ Fast and reliable when you have good data  
> ❌ Requires lots of labeled examples

### 2. 🎮 Reinforcement Learning (RL)  
- The robot learns by **trial and error**, guided by rewards.  
- Example: A robot tries different ways to stand up. Each successful step earns a “reward.” Over time, it learns the best strategy.  
- **Use case**: Walking, balancing, complex manipulation tasks.

> ✅ Great for learning behaviors with no clear “right answer”  
> ❌ Can take thousands of attempts—and real-world trials are slow/risky

> 💡 *Tip*: Many teams train in **simulation first**, then transfer skills to real robots (*sim-to-real transfer*).

### 3. 👥 Imitation Learning  
- The robot **watches and copies** a human (or expert).  
- Example: A human moves a robot arm through a task (like pouring water). The robot records the motion and learns to replay it.  
- **Use case**: Fast skill acquisition, human-robot collaboration.

> ✅ Quick way to teach complex motions  
> ❌ Struggles when the situation changes (e.g., cup is in a new place)

## Why Learning Matters in the Real World

Every home, office, and street is different.  
A robot that **only follows rigid code** will fail when:
- The floor is slippery  
- A chair is moved  
- A new object appears

But a **learning robot** can:
- Adjust its walking gait on carpet vs. tile  
- Recognize a soda can even if it’s never seen that brand  
- Improve its handshake based on user feedback

> 💡 **Key Idea**: Learning turns a machine into an *adaptive agent*—ready for the messy, unpredictable real world.

In the next chapter, we’ll look at **real-world applications** of Physical AI—from elder care to disaster response—and how learning makes them possible.