import random

def spin():
    return random.randint(0, 37)


def hit_half_board():
    return spin() < 18


def hit_third_board():
    return spin() < 12


def hit_square():
    return spin() == 0


def pay_out(bet, hit_fn):
    if hit_fn == hit_half_board:
        return bet
    if hit_fn == hit_third_board:
        return bet * 2
    if hit_fn == hit_square:
        return bet * 35
    raise Exception(hit_fn)


def simulate(balance, bet_amt, hit_fn):
    balances = []
    while balance >= bet_amt:
        # place bet
        balance -= bet_amt
        if hit_fn():
            # pay out, baby!
            balance += bet_amt + pay_out(bet_amt, hit_fn)
        balances.append(balance)
    return balances


def run_n_sims(n_sims, balance, bet_amt, hit_fn):
    return [simulate(balance, bet_amt, hit_fn) for i in range(n_sims)]


def _avg_length(results):
    return sum(len(x) for x in results) / len(results)


def play_as_long_as_possible(n_sims, balance, bet_amt):
    """
    Run simulations for all 3 hit strategies and print the average number of
    rounds that each hit strategy makes it through before going bust.
    """
    # run sims
    results_half = run_n_sims(n_sims, balance, bet_amt, hit_half_board)
    results_third = run_n_sims(n_sims, balance, bet_amt, hit_third_board)
    results_square = run_n_sims(n_sims, balance, bet_amt, hit_square)

    # get average total rounds
    print(f'Avg rounds (half): {_avg_length(results_half)}')
    print(f'Avg rounds (third): {_avg_length(results_third)}')
    print(f'Avg rounds (square): {_avg_length(results_square)}')


def double_up_and_go(n_sims, balance, bet_amt):
    """
    Run simulations for all 3 hit strategies and print the total rounds
    for which the balance ends up greater than 2x the initial balance.
    """
    # run sims
    results_half = run_n_sims(n_sims, balance, bet_amt, hit_half_board)
    results_third = run_n_sims(n_sims, balance, bet_amt, hit_third_board)
    results_square = run_n_sims(n_sims, balance, bet_amt, hit_square)

    half_bet_double_ups = len([x for x in results_half if max(x) >= 2*balance])
    third_bet_double_ups = len([x for x in results_third if max(x) >= 2*balance])
    square_double_ups = len([x for x in results_square if max(x) >= 2*balance])

    print(f'Double up rounds (half): {half_bet_double_ups}')
    print(f'Double up rounds (third): {third_bet_double_ups}')
    print(f'Double up rounds (square): {square_double_ups}')
