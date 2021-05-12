project = "bmc_discovery_pgsq"

app "bmc_discovery_pgsq" {
  labels = {
    "service" = "bmc_discovery_pgsq"
  }

  build {
    use "docker" {}
  }

  deploy {
    use "docker" {
      service_port = 8082
    }
  }
}
