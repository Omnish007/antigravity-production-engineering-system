---
name: Kubernetes
category: deployment
baselineVersion: 1.35.8 (1.34+ compatibility)
lastVerified: '2026-09-22'
reviewAfter: '2026-12-31'
preferredVersion: 1.35.8
supportedVersions:
- 1.35.x
- 1.34.x
- 1.33.x
legacyVersions:
- 1.32.x
prohibitedVersions:
- < 1.32
sources:
- https://kubernetes.io/docs/home/
- https://kubernetes.io/docs/reference/kubernetes-api/
---
# Kubernetes Deployment Profile

## 1. Scope
Applies to containerized applications and services deployed to Kubernetes clusters (EKS, GKE, AKS, or bare-metal).

## 2. Detection Signals
- Files: `k8s/`, `manifests/`, `helm/`, `Chart.yaml`, `kustomization.yaml`
- File patterns: `*.k8s.yaml`, `deployment.yaml`, `service.yaml`

## 3. Supported-Version Policy
- Target: Kubernetes 1.35.8 (with 1.34+ compatibility).

## 4. Core Architectural Guidance
- **Resource Requests & Limits**: Every Pod container must specify both `requests` (CPU and memory for scheduling) and `limits` (to prevent node-level OOM resource starvation).
- **Health Probes**:
  - Configure `livenessProbe` to detect deadlocks and trigger container restart.
  - Configure `readinessProbe` to determine when the container can accept live traffic.
  - Configure `startupProbe` for slow-starting applications to prevent premature liveness kills.
- **Graceful Shutdown**: Implement handling for `SIGTERM` and configure `terminationGracePeriodSeconds` to allow in-flight requests to complete before pod termination.
- **Declarative Configuration**: Use Helm or Kustomize for multi-environment configuration management.

## 5. Security & Performance Guidance
- **Security Context**: Enforce `readOnlyRootFilesystem: true`, `allowPrivilegeEscalation: false`, and run as non-root UID (`runAsNonRoot: true`).
- **Network Policies**: Define Kubernetes `NetworkPolicy` resources to restrict pod-to-pod ingress and egress traffic.
- **Secrets Management**: Integrate with External Secrets Operator or HashiCorp Vault rather than committing plaintext Kubernetes Secret manifests.

## 6. Testing Guidance
- Manifest Linting: Use `kubeconform` or `kubeval` to validate Kubernetes YAML manifests against official schemas.
- Helm Linting: Run `helm lint` and `helm template` for Helm charts.
- Verification: Dry-run apply: `kubectl apply --dry-run=client -f <manifest>`.

## 7. Common Anti-patterns
- Deploying Pods without CPU/memory `requests` and `limits`, causing cluster instability.
- Using identical endpoints for both `livenessProbe` and `readinessProbe`, causing healthy pods to be killed when downstream dependencies are degraded.
- Storing plaintext secrets in Git-tracked Kubernetes manifests.
- Running containers with root privileges (`runAsUser: 0`) or privileged capabilities.

## 8. Official & Local Documentation Discovery
- Official Documentation: https://kubernetes.io/docs/home/
- Kubernetes API Reference: https://kubernetes.io/docs/reference/kubernetes-api/
- Local Inspection: Inspect `k8s/`, `manifests/`, or `helm/` directories.
