# BrainyTicTacToe
BrainyTicTacToe is a Python-based Tic-Tac-Toe game where the AI improves over time by learning from every game you play. It uses Q-learning to remember which moves lead to wins or losses, adapts its strategy, and even explains its reasoning in real-time. Play against the AI, watch it learn, and try to beat it!

# Read
https://en.wikipedia.org/wiki/Q-learning

This project uses **Q-learning**, which is a type of **reinforcement learning**. In simple terms:

-   The AI treats **every board state** as a situation it can be in.

-   For each state, it has **possible actions** (places it can put `O`).

-   It keeps a **Q-table**, which stores "how good each action is in each state" based on past games.

-   When it makes a move and sees the result (win, lose, draw), it **updates the Q-values** using the formula:

The Q-learning update rule used in BrainyTicTacToe is:

$$
Q(s, a) = Q(s, a) + \alpha \cdot \Big( \text{reward} + \gamma \cdot \max Q(s', a') - Q(s, a) \Big)
$$

Where:

-   `s` = current state

-   `a` = action taken

-   `s'` = next state after action

-   `reward` = numeric reward (+1 win, -1 loss, etc.)

-   `alpha` = learning rate (how fast AI learns)

-   `gamma` = discount factor (how much it cares about future rewards)

So basically, **the AI "remembers" which moves were good and gradually gets better**

<img width="1901" height="993" alt="image" src="https://github.com/user-attachments/assets/37087012-94ef-4fb6-b942-154908e925bb" />

