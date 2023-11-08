import networkx as nx


def calculate_optimal_trades(price_schedule, current_charge_state) -> []:
    trading_options_graph = transform_prs_to_graph(price_schedule, 50, 85, 5)

    optimal_trading_path = nx.shortest_path(trading_options_graph, f"0:${current_charge_state}", f"${len(price_schedule)}:45", method="bellman-ford")

    return optimal_trading_path


def transform_prs_to_graph(price_schedule, min_charge_state, max_charge_state, max_change_rate) -> []:
    trading_paths_graph = nx.DiGraph()
    for tradingPeriod in range(len(price_schedule)):
        trading_period_price = price_schedule[tradingPeriod]

        for current_charge_state in range(min_charge_state, max_charge_state):
            for charge_change in range(-max_change_rate, max_change_rate):
                new_charge = current_charge_state + charge_change

                if new_charge < min_charge_state | new_charge > max_charge_state:
                    continue

                cost = charge_change * trading_period_price  # should also add variable network costs

                trading_paths_graph.add_edge(f"${tradingPeriod}_${current_charge_state}", f"${tradingPeriod}:${current_charge_state + charge_change}", weight=cost)

    return trading_paths_graph


price_list = [1, 1, 30, 1, 100, 1, 1, 1]

print(calculate_optimal_trades(price_list, 45))
