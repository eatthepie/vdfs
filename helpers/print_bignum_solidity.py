import json

with open('proof.json', 'rb') as f:
  proof_json = json.load(f)

# Generate the Solidity format
solidity_output = 'BigNumber[] memory v = new BigNumber[]({});\n\n'.format(len(proof_json["v"]))
for i, item in enumerate(proof_json["v"]):
    solidity_output += f'v[{i}] = BigNumber({{\n'
    solidity_output += f'    val: hex"{item["val"]}",\n'
    solidity_output += f'    bitlen: {item["bitlen"]}\n'
    solidity_output += '});\n\n'

# Print the resulting Solidity code
print(solidity_output)
