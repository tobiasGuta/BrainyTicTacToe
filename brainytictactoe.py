import os
import random
import pickle
import time
from datetime import datetime

Q_FILE = "q_table.pkl"
BRAIN_FILE = "ai_brain.log"

alpha = 0.8
gamma = 0.9
DEBUG = True

# Load memory
if os.path.exists(Q_FILE) and os.path.getsize(Q_FILE) > 0:
    with open(Q_FILE, "rb") as f:
        Q = pickle.load(f)
else:
    Q = {}

ai_chat = []  # store on-screen debug chat


def log_brain(msg):
    # Store in terminal chat and file.
    timestamp = datetime.now().strftime("%H:%M:%S")
    entry = f"[{timestamp}] {msg}"
    ai_chat.append(entry)
    if len(ai_chat) > 8:  # limit chat size on screen
        ai_chat.pop(0)
    with open(BRAIN_FILE, "a") as f:
        f.write(entry + "\n")


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def render(board):
    # Draw board and debug chat side-by-side.
    clear()
    print("=== Tic-Tac-Toe (AI Learns While You Play) ===\n")
    for i in range(0, 9, 3):
        print(f" {board[i]} | {board[i+1]} | {board[i+2]} ")
        if i < 6:
            print("---|---|---")

    print("\nAI Brain Log:")
    print("-" * 28)
    for line in ai_chat:
        print(line)
    print("-" * 28)
    print()


def get_state(board):
    return "".join(board)


def available_moves(board):
    return [i for i, s in enumerate(board) if s == " "]


def check_winner(board, player):
    wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
    return any(board[a]==board[b]==board[c]==player for a,b,c in wins)


def get_epsilon():
    return max(0.05, 0.2 - len(Q) / 2000)


def choose_move(board):
    # AI chooses move with visible reasoning.
    state = get_state(board)
    moves = available_moves(board)
    eps = get_epsilon()

    log_brain(f"Thinking about state: {state}")
    time.sleep(0.2)

    if random.random() < eps or state not in Q:
        move = random.choice(moves)
        log_brain(f"Exploring randomly → chose {move}")
        return move

    q_values = {a: Q[state].get(a, 0) for a in moves}
    best = max(q_values, key=q_values.get)
    log_brain(f"Q-values: {q_values}")
    log_brain(f"Best learned move → {best}")
    return best


def update_q(old_state, action, reward, new_state):
    if old_state not in Q:
        Q[old_state] = {a: 0 for a in range(9)}
    if new_state not in Q:
        Q[new_state] = {a: 0 for a in range(9)}

    old = Q[old_state][action]
    future = max(Q[new_state].values()) if Q[new_state] else 0
    new = old + alpha * (reward + gamma * future - old)
    Q[old_state][action] = new
    log_brain(f"Updated Q[{action}] → {new:.3f} (was {old:.3f}, r={reward:+.2f})")


def save_q():
    with open(Q_FILE, "wb") as f:
        pickle.dump(Q, f)
    log_brain(f"Saved {len(Q)} learned states to memory.")


def ai_smart_move(board, ai, player):
    # Adds short-term tactics + logs reasoning.
    moves = available_moves(board)
    for m in moves:
        temp = board.copy()
        temp[m] = ai
        if check_winner(temp, ai):
            log_brain(f"Found winning move → {m}")
            return m

    for m in moves:
        temp = board.copy()
        temp[m] = player
        if check_winner(temp, player):
            log_brain(f"Blocking player's threat → {m}")
            return m

    log_brain("No immediate win/block — consulting Q-memory")
    return choose_move(board)


def position_reward(pos):
    center = 4
    corners = [0, 2, 6, 8]
    if pos == center:
        return 0.2
    elif pos in corners:
        return 0.1
    else:
        return -0.1


def play():
    board = [" "] * 9
    player, ai = "X", "O"
    ai_memory = []

    log_brain("New game started.")
    while True:
        render(board)
        print("Positions:\n 1 | 2 | 3 \n---|---|---\n 4 | 5 | 6 \n---|---|---\n 7 | 8 | 9 \n")
        try:
            move = int(input("Your move (1–9): ")) - 1
        except ValueError:
            continue
        if move not in range(9) or board[move] != " ":
            continue
        board[move] = player

        if check_winner(board, player):
            render(board)
            print("You win!")
            log_brain("AI lost this game — learning from loss.")
            for i, (s, a) in enumerate(reversed(ai_memory)):
                penalty = -1 * (0.8 ** i)
                update_q(s, a, penalty, get_state(board))
                log_brain(f"Learning from loss: penalized move {a} with {penalty:.3f}")
            save_q()
            break

        if " " not in board:
            render(board)
            print("Draw.")
            for s, a in ai_memory:
                update_q(s, a, 0, get_state(board))
            save_q()
            break

        old_state = get_state(board)
        action = ai_smart_move(board, ai, player)
        board[action] = ai
        new_state = get_state(board)
        ai_memory.append((old_state, action))
        update_q(old_state, action, position_reward(action), new_state)

        if check_winner(board, ai):
            render(board)
            print("AI wins!")
            for s, a in ai_memory:
                update_q(s, a, 1, new_state)
            save_q()
            break
        elif " " not in board:
            render(board)
            print("Draw.")
            for s, a in ai_memory:
                update_q(s, a, 0, new_state)
            save_q()
            break


if __name__ == "__main__":
    while True:
        play()
        again = input("\nPlay again? (y/n): ").lower()
        if again != "y":
            break
