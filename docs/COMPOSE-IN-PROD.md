# Docker Compose in Production

For the simplest web applications we can often getaway with just using `docker compose`. There are a few considerations to be made, but for the most of the setup presents itself as closely as possible to the full Kubernetes provisioned environment. This guide will walk you through the configuration of a production ready Docker Compose environment.

What we are missing:

- Secret are stored in an `.env` file on the server, at present Linode does not provide a way to pass environment variables through a management secrets services. We could look into services like Hashicorp's `Vault`.
- Create a Terraform template to orchestrate the creation of the Linode instance and the deployment of the application. This will be taken up by the `lab-tf-linode`


