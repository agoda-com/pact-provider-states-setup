Pact provider states setup
==========================

**Pact provider states setup** is a simple web service adding support for Pact
[provider states](https://docs.pact.io/getting_started/provider_states) setup.

Using this tool, you can add support for provider states to your Pact provider
app without modifying it.

It currently supports only forwarding arbitrary GraphQL queries and mutations to
a given path relative to the provider base URL. This may be sufficient to set
initial data for your Pact verification to succeed.

Example
-------

### 1. Prerequisites

Suppose that you have:

* A Pact provider: a web service listening at `http://myprovider:12345/` and
  exposing a GraphQL endpoint `/my/graphql/endpoint`
* A Pact consumer calling this endpoint: in this example, we use a C# app using
  [PactNet](https://www.nuget.org/packages/PactNet/) for Pact support, but the
  concept should apply to any consumer app using a stack with Pact V3 support

### 2. Generating a Pact contract with provider state

Get a `myconsumer-myprovider.json` contract by running Pact verification from
tests in your consumer app. A Pact provider state is added to a request via the
`Given` method on the pact builder, like this:

```cs
myPactBuilder
    .UponReceiving("My request")
    .Given("GraphQL query on /my/graphql/endpoint", new Dictionary<string, string>
    {
        {
            "query",
            $@"
            mutation {{
                MyResourceMutation(id: 123, value: ""My value"") {{ id }}
            }}
            "
        }
    })
    .WithRequest(System.Net.Http.HttpMethod.Post, "/some/graphql/endpoint")
    .WithBody($@"
        query {{
            MyResource(id: 123) {{ id, value }}
        }}
    ", "application/json")
    .WillRespond()
    .WithStatus(System.Net.HttpStatusCode.OK)
    .WithJsonBody(new
    {
        data = new
        {
            MyResource = new { id = 123, value = "My value" }
        }
    });
```

### 3. Spawning *Pact provider states setup*

Spawn *Pact provider states setup* using Docker and pass the the base URL to
your provider app via the `PROVIDER_BASE_URL` environment variable, like this:

```sh
docker container run --rm --detach \
  --env PROVIDER_BASE_URL='http://myprovider:12345/' \
  --name pact-provider-states-setup \
  --network host \
  pact-provider-states-setup:latest
```

*Pact provider states setup* is now listening at `http://localhost:8000/`.

### 4. Verify a Pact contract using provider state

Run Pact provider verification using [Pact command line
tools](https://docs.pact.io/implementation_guides/cli), like this:

```sh
pact verify \
  --provider-base-url='http://my-provider:12345/' \
  --provider-states-setup-url='http://localhost:8000/' \
  /path/to/myconsumer-myprovider.json
```

Before each Pact contract interaction, the GraphQL mutation, passed as a Pact
provider state, is first forwarded to your provider app before the Pact
verification is performed.

### 5. Conclusion

Using Pact provider states and *Pact provider states setup* allows you to **set,
from your consumer app, the state of your provider app without modifying it**.

This can help stabilising Pact verification on provider side.
