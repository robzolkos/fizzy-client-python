# Integration Tests

This directory contains integration tests that run against the real Fizzy API.

## Prerequisites

Before running the integration tests, you need to set up the following environment variables:

```bash
export FIZZY_API_TOKEN="your-personal-access-token"
export FIZZY_ACCOUNT_SLUG="your-account-slug"
export FIZZY_TEST_BOARD_ID="board-id-for-testing"
```

## Running the Tests

```bash
python integration_tests/run_tests.py
```

## Test Behavior

The integration tests will:

1. Verify your authentication by checking your identity
2. List boards in your account
3. Create, update, and delete test cards
4. Create, update, and delete test comments
5. Create, update, and delete test steps

**Warning**: The tests will create temporary resources (cards, comments, steps) in your test board. These resources will be cleaned up at the end of each test.

## Safety

- Always use a dedicated test board for integration tests
- The tests never modify or delete existing resources
- All created resources have "TEST:" prefix in their titles for easy identification
