import networkx as nx


def weight_func(start, end, edge_attributes): return edge_attributes["weight"]


def calculate_optimal_trades(price_schedule, current_charge_state, min_charge_state, max_charge_state, end_charge_state, max_change_rate) -> []:
    trading_options_graph = transform_price_schedule_to_graph(price_schedule, min_charge_state, end_charge_state, max_change_rate)

    optimal_trading_path = nx.shortest_path(trading_options_graph, f"0:{current_charge_state}", f"{len(price_schedule)}:{max_charge_state}", weight_func, method="bellman-ford")
    length = nx.shortest_path_length(trading_options_graph, f"0:{current_charge_state}", f"{len(price_schedule)}:{max_charge_state}", weight_func, method="bellman-ford")
    print(length)
    return optimal_trading_path


def transform_price_schedule_to_graph(price_schedule, min_charge_state, max_charge_state, max_change_rate) -> nx.DiGraph:
    trading_paths_graph = nx.DiGraph()

    for tradingPeriod in range(len(price_schedule)):
        trading_period_price = price_schedule[tradingPeriod]

        for current_charge_state in range(min_charge_state, max_charge_state + 1):
            for charge_change in range(-max_change_rate, max_change_rate + 1):
                new_charge = current_charge_state + charge_change

                if new_charge < min_charge_state or new_charge > max_charge_state:
                    continue

                source = f"{tradingPeriod}:{current_charge_state}"
                destination = f"{tradingPeriod + 1}:{current_charge_state + charge_change}"
                cost = charge_change * trading_period_price  # should also add variable network costs

                trading_paths_graph.add_edge(source, destination, weight=cost)

    return trading_paths_graph


price_list = [146, 146, 146, 146, 146, 146, 135.22, 146, 145.77, 146, 143.07, 145.74, 143.16, 143.01, 142.97, 142.97, 142.66, 145.96, 146, 146, 131.89, 146, 144.37, 132.23, 121.05, 108.35, 90.01, 90.32, 89.27, 91.62, 91.62, 121.24, 109.13,
              109.12, 109.07, 108.93, 100.75, 108.84, 108.99, 88.8, 85.16, 85.28, 97.22, 111.5, 114.68, 107.92, 110.32, 122.6, 138.26, 146, 146, 119.52, 146, 146, 146, 146.29, 146, 146, 146, 146, 102.94, 100.38, 100.37, 100.46, 117.7, 146,
              146, 95.56, 89.04, 88.55, 88.91]

print(calculate_optimal_trades(price_list, 50, 30, 90, 50, 5))
