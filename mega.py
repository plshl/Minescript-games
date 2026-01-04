# Mega Minigames Script for Minescript
import random
import minescript # type: ignore
from minescript import chat, echo, EventQueue # type: ignore
import time

# --- Coin Flip Minigame ---
def coinflip_handler(msg_content, username):
    if msg_content.lower().startswith("!cf") or msg_content.lower().startswith("!coinflip"):
        coinside = random.choice(["heads", "tails"])
        chat(f"{username} Flipped a coin that landed on {coinside}")
        return True
    return False

# --- Quick Math Minigame ---
active_question = None
active_answer = None
math_answered = False

def generate_question():
    a = random.randint(1, 20)
    b = random.randint(1, 20)
    op = random.choice(['+', '-', '*'])
    if op == '+':
        return f"What is {a} + {b}?", a + b
    elif op == '-':
        return f"What is {a} - {b}?", a - b
    else:
        return f"What is {a} * {b}?", a * b

def math_handler(msg_content, username):
    global active_question, active_answer, math_answered
    if msg_content.lower().startswith("!math") and not active_question:
        question, answer = generate_question()
        active_question = question
        active_answer = answer
        math_answered = False
        chat(f"[Quick Math] {question} (First correct answer wins!)")
        return True
    if active_question and not math_answered:
        try:
            if int(msg_content) == active_answer:
                chat(f"[Quick Math] {username} answered correctly! The answer was {active_answer}.")
                active_question = None
                active_answer = None
                math_answered = True
                return True
        except ValueError:
            pass
    return False

# --- Blackjack Minigame ---
def draw_card():
    ranks = [2,3,4,5,6,7,8,9,10,10,10,10,11] # 10, J, Q, K, A
    return random.choice(ranks)

blackjack_cooldowns = {}
roulette_cooldowns = {}
COOLDOWN_SECONDS = 240  # 4 minutes

def blackjack_handler(msg_content, username):
    if msg_content.lower().startswith("!blackjack") or msg_content.lower().startswith("!21"):
        now = time.time()
        last = blackjack_cooldowns.get(username, 0)
        if now - last < COOLDOWN_SECONDS:
            remaining = int(COOLDOWN_SECONDS - (now - last))
            chat(f"[BJ] {username}, please wait {remaining//60}:{remaining%60:02d} before playing again.")
            return True
        blackjack_cooldowns[username] = now
        player_hand = [draw_card(), draw_card()]
        dealer_hand = [draw_card(), draw_card()]
        player_total = sum(player_hand)
        dealer_total = sum(dealer_hand)
        chat(f"[BJ] {username}: Hand: {player_hand} ({player_total}) | Dealer: [{dealer_hand[0]}, ?]")
        # Simple auto-play: player hits if under 17, stands otherwise
        while player_total < 17:
            card = draw_card()
            player_hand.append(card)
            player_total = sum(player_hand)
            chat(f"[BJ] {username}: Hit {card}, total {player_total}")
            if player_total > 21:
                chat(f"[BJ] {username}: Bust! Dealer wins.")
                return True
        chat(f"[BJ] {username}: Stand {player_total}")
        # Dealer plays
        chat(f"[BJ] {username}: Dealer: {dealer_hand} ({dealer_total})")
        while dealer_total < 17:
            card = draw_card()
            dealer_hand.append(card)
            dealer_total = sum(dealer_hand)
            chat(f"[BJ] {username}: Dealer hit {card}, total {dealer_total}")
            if dealer_total > 21:
                chat(f"[BJ] {username}: Dealer busts! You win.")
                return True
        chat(f"[BJ] {username}: Dealer stands {dealer_total}")
        # Decide winner
        if player_total > dealer_total:
            chat(f"[BJ] {username}: Win! {player_total} vs {dealer_total}")
        elif player_total < dealer_total:
            chat(f"[BJ] {username}: Lose! {dealer_total} vs {player_total}")
        else:
            chat(f"[BJ] {username}: Tie! {player_total}")
        return True
    return False

# --- Unscramble Minigame ---
unscramble_words = [
    "contraption", "deployer", "shaft", "cogwheel", "flywheel", "waterwheel", "mechanical", "mixer", "press", "drill", "saw", "glue", "wrench", "zinc", "crushingwheel", "blazeburner", "sequencer", "gearbox", "encasedfan", "andesite", "brass", "rotation", "stress", "kinetic", "pulley", "belt", "funnel", "chute", "depot", "millstone", "basin", "spout", "pipe", "valve", "tank", "steamengine", "generator", "elevator", "cartassembler", "track", "train", "station"
]
active_word = None
scrambled_word = None
unscramble_answered = False

def scramble(word):
    word_letters = list(word)
    random.shuffle(word_letters)
    return ''.join(word_letters)

def unscramble_handler(msg_content, username):
    global active_word, scrambled_word, unscramble_answered
    if (msg_content.lower().startswith("!unscramble") or msg_content.lower().startswith("!uc")) and not active_word:
        active_word = random.choice(unscramble_words)
        scrambled_word = scramble(active_word)
        unscramble_answered = False
        chat(f"[Unscramble] Unscramble this Create Mod word: {scrambled_word} (First correct answer wins!)")
        return True
    if active_word and not unscramble_answered:
        answer = msg_content.lower().replace(" ", "")
        if answer == active_word:
            chat(f"[Unscramble] {username} unscrambled it! The word was '{active_word}'.")
            active_word = None
            scrambled_word = None
            unscramble_answered = True
            return True
    return False

# --- Guess the Number Minigame ---
guess_active = False
guess_number = None
guess_answered = False
guess_min = 1
guess_max = 100

def guess_handler(msg_content, username):
    global guess_active, guess_number, guess_answered, guess_min, guess_max
    if msg_content.lower().startswith("!guess") and not guess_active:
        parts = msg_content.lower().split()
        if len(parts) > 1 and parts[1] == "easy":
            guess_min = 1
            guess_max = 10
            chat("[Guess the Number] (Easy) I'm thinking of a number between 1 and 10. First to guess it wins!")
        else:
            guess_min = 1
            guess_max = 100
            chat("[Guess the Number] (Hard) I'm thinking of a number between 1 and 100. First to guess it wins!")
        guess_number = random.randint(guess_min, guess_max)
        print(f"[Guess the Number] (Console) The number is: {guess_number}")
        guess_active = True
        guess_answered = False
        return True
    if guess_active and not guess_answered:
        try:
            if int(msg_content) == guess_number:
                chat(f"[Guess the Number] {username} guessed it! The number was {guess_number}.")
                guess_active = False
                guess_number = None
                guess_answered = True
                return True
        except ValueError:
            pass
    return False


# --- Roulette Minigame ---
roulette_colors = ["red", "black", "green"]
roulette_numbers = list(map(str, range(0, 37)))
roulette_options = roulette_colors + roulette_numbers

def roulette_handler(msg_content, username):
    if msg_content.lower().startswith("!roulette"):
        now = time.time()
        last = roulette_cooldowns.get(username, 0)
        if now - last < COOLDOWN_SECONDS:
            remaining = int(COOLDOWN_SECONDS - (now - last))
            chat(f"[Roulette] {username}, please wait {remaining//60}:{remaining%60:02d} before playing again.")
            return True
        roulette_cooldowns[username] = now
        parts = msg_content.lower().split()
        if len(parts) < 2 or parts[1] not in roulette_options:
            chat("[Roulette] Usage: !roulette <red|black|green|0-36>")
            return True
        player_choice = parts[1]
        spin_number = random.randint(0, 36)
        if spin_number == 0:
            spin_color = "green"
        elif spin_number in [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]:
            spin_color = "red"
        else:
            spin_color = "black"
        if player_choice in roulette_colors:
            if player_choice == spin_color:
                chat(f"[Roulette] {username} bet on {player_choice} and WON! The ball landed on {spin_color} {spin_number}.")
            else:
                chat(f"[Roulette] {username} bet on {player_choice} and lost. The ball landed on {spin_color} {spin_number}.")
        else:
            if player_choice == str(spin_number):
                chat(f"[Roulette] {username} bet on {player_choice} and WON! The ball landed on {spin_color} {spin_number}.")
            else:
                chat(f"[Roulette] {username} bet on {player_choice} and lost. The ball landed on {spin_color} {spin_number}.")
        return True
    return False

# --- Main Event Loop ---
chat("[Mega Minigames] Script started! Available commands: !cf, !coinflip, !math, !unscramble, !uc, !guess, !guess easy, !guess hard, !roulette <red|black|green|0-36>(4 min cooldown), !blackjack/!21(4 min cooldown)")
with EventQueue() as event_queue:
    event_queue.register_chat_listener()
    while True:
        event = event_queue.get()
        if event.type == minescript.EventType.CHAT:
            msg = event.message.strip()
            username = "Someone"
            msg_content = msg
            if msg.startswith("<") and ">" in msg:
                username = msg[1:msg.index(">")].strip()
                msg_content = msg[msg.index(">")+1:].strip()
            # Try each minigame handler
            if coinflip_handler(msg_content, username):
                continue
            if math_handler(msg_content, username):
                continue
            if unscramble_handler(msg_content, username):
                continue
            if guess_handler(msg_content, username):
                continue
            if roulette_handler(msg_content, username):
                continue
            if blackjack_handler(msg_content, username):
                continue
