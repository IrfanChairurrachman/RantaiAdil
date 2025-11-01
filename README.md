# RantaiAdil

> A decentralized payment splitting smart contract on Algorand blockchain

[![Algorand](https://img.shields.io/badge/Algorand-000000?style=for-the-badge&logo=algorand&logoColor=white)](https://www.algorand.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![AlgoKit](https://img.shields.io/badge/AlgoKit-00BFFF?style=for-the-badge)](https://github.com/algorandfoundation/algokit-cli)

## Overview

**RantaiAdil** (meaning "Fair Chain" in Indonesian) is a transparent and trustless payment splitting dApp built on the Algorand blockchain. It enables project managers to fairly distribute payments among multiple contributors based on predefined share percentages, ensuring everyone gets their fair share automatically.

### Deployed Smart Contract

**Testnet Application ID:** [748956819](https://lora.algokit.io/testnet/application/748956819)

View live contract: [https://lora.algokit.io/testnet/application/748956819](https://lora.algokit.io/testnet/application/748956819)

## What It Does

RantaiAdil solves the common problem of manual payment distribution in collaborative projects. Whether you're working on a freelance project, a software development team, or a creative collaboration, RantaiAdil ensures:

- **Transparent Distribution**: All contributors know exactly what percentage they'll receive
- **Automated Payouts**: No manual calculations or multiple transactions needed
- **Trustless Execution**: Smart contract guarantees everyone gets paid once project completes
- **Immutable Records**: All transactions are recorded on the Algorand blockchain

## Key Features

### For Project Managers
- Set up project with manager and client addresses
- Add multiple contributors with custom share percentages (0-100%)
- Lock contributor list to prevent unauthorized modifications
- Complete project and trigger automatic payouts

### For Contributors
- Guaranteed payment according to agreed share percentage
- Transparent tracking of project status
- Instant payout upon project completion
- No middleman or manual payment processing

### For Clients
- Fund projects securely through the smart contract
- Funds are held safely until project completion
- Transparent view of all contributors and their shares
- Assurance that funds will be distributed fairly

### Smart Contract Features
- **Role-Based Access Control**: Only authorized parties can perform specific actions
- **State Validation**: Prevents duplicate payments and unauthorized modifications
- **Percentage Validation**: Ensures total shares equal exactly 100%
- **Minimum Funding**: Requires at least 1 ALGO to prevent dust transactions
- **Payment Tracking**: Tracks which contributors have been paid
- **Status Monitoring**: Real-time project status queries

## How It Works

### Workflow

```
1. Setup Project
   └─> Manager initializes project with manager & client addresses

2. Add Contributors
   └─> Manager adds contributors with share percentages
   └─> Example: Developer (40%), Designer (30%), Tester (30%)

3. Lock Contributors
   └─> Manager locks the list (validates total = 100%)
   └─> No more contributors can be added

4. Fund Project
   └─> Client sends payment to smart contract
   └─> Funds are held securely

5. Complete & Payout
   └─> Manager or Client marks project complete
   └─> Smart contract automatically distributes funds to all contributors
   └─> Each contributor receives their exact percentage
```

## Smart Contract Methods

### Administrative Methods

| Method | Caller | Description |
|--------|--------|-------------|
| `setup_project(manager, client)` | Anyone (once) | Initialize project with manager and client addresses |
| `add_contributor(address, percentage)` | Manager | Add a contributor with their share percentage |
| `lock_contributors()` | Manager | Lock contributor list and validate total = 100% |

### Transaction Methods

| Method | Caller | Description |
|--------|--------|-------------|
| `fund_project(payment)` | Client | Fund the project with ALGO (min 1 ALGO) |
| `complete_and_payout()` | Manager/Client | Complete project and distribute funds automatically |

### Query Methods

| Method | Caller | Description |
|--------|--------|-------------|
| `get_project_status()` | Anyone | Get current project status |
| `get_contributor_count()` | Anyone | Get total number of contributors |
| `hello(name)` | Anyone | Test method for verification |

## Technical Stack

- **Blockchain**: Algorand
- **Smart Contract Language**: Algorand Python (PuyaPy)
- **Framework**: AlgoKit
- **Python Version**: 3.12+
- **Contract Type**: ARC4 Application

## Getting Started

### Prerequisites

- [Python 3.12](https://www.python.org/downloads/) or later
- [Docker](https://www.docker.com/) (for LocalNet testing)
- [AlgoKit CLI](https://github.com/algorandfoundation/algokit-cli#install) v2.0.0+
- [Poetry](https://python-poetry.org/docs/#installation) v1.2+

### Installation

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd RantaiAdil/projects/RantaiAdil
   ```

2. **Bootstrap the Project**
   ```bash
   algokit project bootstrap all
   ```
   This will install all dependencies and set up your Python virtual environment.

3. **Configure Environment**
   ```bash
   algokit generate env-file -a target_network localnet
   ```

4. **Start LocalNet**
   ```bash
   algokit localnet start
   ```

### Build & Deploy

#### Build the Smart Contract
```bash
algokit project run build
```

#### Deploy to LocalNet
```bash
algokit project deploy localnet
```

#### Deploy to TestNet
```bash
algokit project deploy testnet
```

## Development

### Project Structure
```
smart_contracts/
├── rantai_adil/
│   ├── contract.py          # Main smart contract
│   └── deploy_config.py     # Deployment configuration
├── __main__.py              # Build script
└── artifacts/               # Compiled contract outputs
```

### Running Tests
```bash
# Add your test commands here
poetry run pytest
```

### Code Tour
For an interactive walkthrough of the codebase, install the [CodeTour extension](https://marketplace.visualstudio.com/items?itemName=vsls-contrib.codetour) and open `.tours/getting-started-with-your-algokit-project.tour`.

## Usage Example

### Python SDK Example
```python
from algokit_utils import ApplicationClient
from algosdk.v2client.algod import AlgodClient

# Initialize Algod client
algod_client = AlgodClient("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "http://localhost:4001")

# Create application client
app_client = ApplicationClient(
    algod_client=algod_client,
    app_id=748956819,  # TestNet app ID
    # ... other configuration
)

# 1. Setup project
app_client.call("setup_project", manager=manager_address, client=client_address)

# 2. Add contributors
app_client.call("add_contributor", contributor_address=dev_address, share_percentage=40)
app_client.call("add_contributor", contributor_address=designer_address, share_percentage=30)
app_client.call("add_contributor", contributor_address=tester_address, share_percentage=30)

# 3. Lock contributors
app_client.call("lock_contributors")

# 4. Fund project (client sends payment)
# //paste your code

# 5. Complete and payout
app_client.call("complete_and_payout")
```

## Security Considerations

### Access Control
- Only the **manager** can add contributors and lock the list
- Only the **client** can fund the project
- Only **manager or client** can complete and trigger payouts

### Validations
- Project can only be initialized once
- Contributors cannot be added after locking
- Total share percentages must equal exactly 100%
- Minimum funding is 1 ALGO (1,000,000 microAlgos)
- Project cannot be completed twice
- Payment receiver must be the smart contract address

### State Management
- Immutable roles after setup
- Locked contributor list prevents tampering
- Payment tracking prevents double-spending
- Completion flag prevents re-execution

## Debugging

This project supports the AlgoKit AVM Debugger extension for VS Code:

1. Install [AlgoKit AVM Debugger](https://marketplace.visualstudio.com/items?itemName=algorandfoundation.algokit-avm-vscode-debugger)
2. Use `F5` or `Debug TEAL via AlgoKit AVM Debugger` launch configuration
3. Select a trace file and debug your smart contract execution

## Use Cases

- **Freelance Projects**: Split payments between developers, designers, and project managers
- **Open Source Development**: Distribute bounties among multiple contributors
- **Content Creation**: Share revenue between writers, editors, and marketers
- **Collaborative Art**: Split NFT sales among artists and creators
- **Consulting Teams**: Divide project fees based on contribution percentage
- **Bug Bounty Programs**: Distribute rewards to security researchers

## Roadmap

- [ ] Add support for milestone-based payments
- [ ] Implement time-locked fund releases
- [ ] Add dispute resolution mechanism
- [ ] Support for multiple funding rounds
- [ ] Integration with Algorand Standard Assets (ASA)
- [ ] Web-based UI for easier interaction
- [ ] Mobile app support

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Resources

- [Algorand Developer Portal](https://dev.algorand.co/)
- [AlgoKit Documentation](https://github.com/algorandfoundation/algokit-cli/blob/main/docs/algokit.md)
- [Algorand Python Documentation](https://github.com/algorandfoundation/puya)
- [AlgoKit Utils](https://github.com/algorandfoundation/algokit-utils-py)

## License

XXX

## Support

For questions and support:
- Open an issue on GitHub
- Check the [AlgoKit documentation](https://github.com/algorandfoundation/algokit-cli)
- Join the [Algorand Discord](https://discord.gg/algorand)

---

**Built with ❤️ on Algorand using AlgoKit**
