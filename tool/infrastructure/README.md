[![Terraform Lint and Format Check](https://github.com/susumutomita/ai-baseball-coach/actions/workflows/terraform-lint-format.yml/badge.svg?branch=main)](https://github.com/susumutomita/ai-baseball-coach/actions/workflows/terraform-lint-format.yml)

# Auth0 Configuration with Terraform

This repository provides configurations for setting up Auth0 using Terraform.

## Note

This setup is intended to be provisioned using Terraform Cloud. It is not designed for provisioning directly from a local environment.

## Prerequisites

- Terraform installed
- An active Auth0 account

## Setup

1. Clone the repository.

```bash
git clone <repository URL>
```

2. Create a `.env` file in the root directory of the project with the following content:

```bash
TF_VAR_domain=your_auth0_domain
TF_VAR_client_id=your_client_id
TF_VAR_client_secret=your_client_secret
```

3. Make the script `build.sh` executable.

```bash
chmod +x build.sh
```

## Usage

Load the environment variables first. Then, execute Terraform commands.

```bash
./build.sh apply
```

The above command is an example of executing the `apply` command of Terraform. You can pass other Terraform commands as arguments as needed.

## Caution

- Do not commit the `.env` file to public repositories as it contains sensitive information.
- Use build.sh to load the environment variables. This allows Terraform to access the Auth0 configuration information.
