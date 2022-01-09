Micrometer has a MeterRegistry implementation called HealthMeterRegistry (available in the io.micrometer:micrometer-registry-health module) specifically to convert metrics data into availability signals that can be mapped to health indicators watched by load balancers.
Micrometer provides out-of-the-box SLOs that are known to be applicable to a broad range of Java applications

```
HealthMeterRegistry registry = HealthMeterRegistry
  .builder(HealthConfig.DEFAULT)
  .serviceLevelObjectives(JvmServiceLevelObjectives.MEMORY)
  .serviceLevelObjectives(JvmServiceLevelObjectives.ALLOCATIONS)
  .serviceLevelObjectives(OperatingSystemServiceLevelObjectives.DISK)
  .build();
```
We define an api.utilization SLO to support sampling utilization data from health check endpoint
```
@Configuration
class UtilizationServiceLevelObjective {
  @Bean
  ServiceLevelObjective apiUtilization() {
      return ServiceLevelObjective
        .build("api.utilization")
        .baseUnit("requests")
        .failedMessage("Rate limit to 10,000 requests/second.")
        .count(s -> s.name("http.server.requests")
          .tag("uri", "/persons")
          .tag("outcome", "SUCCESS")
        )
        .isLessThan(10_000);
  }
}
```
