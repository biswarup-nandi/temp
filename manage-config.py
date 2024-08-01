import json
import re
import sys
import os

def replace_values(config_file, policy_dir, env, system):
    # Load the config file
    with open(config_file, 'r') as file:
        config_data = json.load(file)

    # Define the pattern to search for
    pattern = re.compile(r'!(\w+)\+(\S+)')

    # Function to recursively search and replace values
    def search_and_replace(data):
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    search_and_replace(value)
                elif isinstance(value, str):
                    match = pattern.match(value)
                    if match:
                        string1, string2 = match.groups()
                        filename = f"ma_{system}_{string1}.json"
                        policy_file = os.path.join(policy_dir, filename)
                        with open(policy_file, 'r') as pf:
                            policy_data = json.load(pf)
                        policy_value = policy_data[string2].get('value', policy_data[string2].get('defaultValue'))
                        data[key] = policy_value
        elif isinstance(data, list):
            for index, item in enumerate(data):
                if isinstance(item, (dict, list)):
                    search_and_replace(item)
                elif isinstance(item, str):
                    match = pattern.match(item)
                    if match:
                        string1, string2 = match.groups()
                        filename = f"ma_{system}_{string1}.json"
                        policy_file = os.path.join(policy_dir, filename)
                        with open(policy_file, 'r') as pf:
                            policy_data = json.load(pf)
                        policy_value = policy_data[string2].get('value', policy_data[string2].get('defaultValue'))
                        data[index] = policy_value

    # Start the replacement process
    search_and_replace(config_data)

    # Save the updated config file
    with open(config_file, 'w') as file:
        json.dump(config_data, file, indent=4)

def main():
    if len(sys.argv) != 3:
        print("Usage: python manage-config.py <work/nonprod/prod> <edc>")
        sys.exit(1)

    env = sys.argv[1]
    system = sys.argv[2]

    config_file = f"config/json_config/{env}.json"
    policy_dir = f"policies/{system}"

    if not os.path.exists(config_file):
        print(f"Config file {config_file} does not exist.")
        sys.exit(1)
    if not os.path.isdir(policy_dir):
        print(f"Policy directory {policy_dir} does not exist.")
        sys.exit(1)

    replace_values(config_file, policy_dir, env, system)
    print(f"Config file {config_file} has been updated successfully.")

if __name__ == "__main__":
    main()
