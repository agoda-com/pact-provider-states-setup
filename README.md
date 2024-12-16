# pact-provider-states-setup: Your Provider States Made Easy! 🎯
## Overview
Welcome to pact-provider-states-setup, an open-source service that makes handling Pact provider states as easy as ordering takeout! We know setting up provider states for Pact verification can be tricky - it's like trying to set up a perfect game of Jenga. That's why we've created this simple web service that adds provider states support without requiring you to modify your existing provider application.

Currently, we're laser-focused on GraphQL, supporting forwarding of queries and mutations to your provider's endpoints. Think of it as your GraphQL traffic controller, making sure your test data is right where it needs to be for successful Pact verification.

## Latest Release
Find our latest version strutting its stuff on Docker Hub:
- [Docker Hub](https://hub.docker.com/r/agoda/pact-provider-states-setup)

## Features
- **Zero Provider Modification**: Add provider states support without touching your provider app. It's like adding a turbo boost without opening the hood!
- **GraphQL Support**: Seamlessly forward your GraphQL queries and mutations. We speak GraphQL fluently!
- **Docker Ready**: Deploy faster than you can say "docker run". Because who has time for complex setups?

## Requirements
- Docker (Because containers are life 🐳)
- A Pact provider application with a GraphQL endpoint
- A burning desire to make your Pact verification more reliable

## Quick Start
### 1. Fire Up the Engine
Launch our service with Docker faster than you can brew your morning coffee:
```sh
docker container run --rm --detach \
  --env PROVIDER_BASE_URL='http://myprovider:12345/' \
  --name pact-provider-states-setup \
  --network host \
  pact-provider-states-setup:latest
```

### 2. Point Your Pact Verification
Tell your Pact verifier where to find us:
```sh
pact verify \
  --provider-base-url='http://my-provider:12345/' \
  --provider-states-setup-url='http://localhost:8000/' \
  /path/to/your-pact-contract.json
```

## How It Works
Think of us as your provider state concierge:
1. You define your provider states in your consumer tests
2. We catch the provider state setup requests
3. We forward your GraphQL operations to your provider
4. Your Pact verification runs smoothly with the right data in place

## Contributing
Got ideas? Found a bug? Want to add support for more operations? We love contributions! Check out our [Contributing Guide](CONTRIBUTING.md) to get started. Because making Pact testing better is a team sport! 🏆

## And Finally...
Remember, good provider states are like good pizza toppings - they need to be just right for everything to work perfectly. With pact-provider-states-setup, you'll never have to worry about getting those toppings wrong again!

Happy testing, and may your Pact verifications always be green! 💚

Made with ❤️ by the Agoda Dev Team
