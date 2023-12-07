import json

def read_plan_file(file_path):
    with open(file_path, 'r') as file:
        plan_data = json.load(file)
    return plan_data

def split_mission_items(plan_data, num_drones):
    mission_items = plan_data["mission"]["items"][2]["TransectStyleComplexItem"]["Items"]
    divided_items = [[] for _ in range(num_drones)]
    number_of_mission_items = len(mission_items)
    each_drone_mission_item_base = number_of_mission_items / num_drones

    drone_index = 0

    for item in mission_items:
        divided_items[drone_index].append(item)
        if len(divided_items[drone_index]) > each_drone_mission_item_base and drone_index != num_drones - 1:
            drone_index += 1

    sub_plans = []
    for items in divided_items:
        sub_plan = plan_data.copy()
        sub_plan["mission"]["items"] = items
        sub_plans.append(sub_plan)


    # now, let's do the visualization part.



    return sub_plans

def save_subplans(sub_plans, base_file_path):
    subplan_file_paths = []
    for i, sub_plan in enumerate(sub_plans):
        subplan_file_path = f"{base_file_path}_subplan_{i+1}.plan"
        with open(subplan_file_path, 'w') as file:
            json.dump(sub_plan, file, indent=4)
        subplan_file_paths.append(subplan_file_path)
    return subplan_file_paths

if __name__ == "__main__":
    file_path = "/home/neil/test/test.plan"
    num_drones = 3
    base_file_path = "/home/neil/test/"

    plan_data = read_plan_file(file_path)
    sub_plans = split_mission_items(plan_data, num_drones)
    subplan_file_paths = save_subplans(sub_plans, base_file_path)

    print("Sub-plan files saved:")
    for path in subplan_file_paths:
        print(path)
