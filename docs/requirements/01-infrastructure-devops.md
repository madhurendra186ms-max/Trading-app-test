# Module 1 — Infrastructure & DevOps

## Purpose
Provide the free, self-hosted compute/network/storage foundation and app runtime.

## Responsibilities
- Provision OpenStack VMs, deploy K3s cluster, manage Helm charts, CI/CD, monitoring.

## Functional Requirements
- FR1: Provision compute/network/storage via OpenStack (Nova, Neutron, Cinder).
- FR2: Deploy K3s cluster across OpenStack VMs.
- FR3: Automate deployments via GitHub Actions + Helm/ArgoCD.
- FR4: Centralized logging and metrics (Prometheus + Grafana).

## Non-Functional Requirements
- NFR1: Zero licensing cost (fully open-source).
- NFR2: Cluster must tolerate single-node failure.
- NFR3: Deployment rollback capability.

## Inputs / Outputs
- Input: none (foundation layer).
- Output: running K3s cluster + CI/CD pipeline available to all other modules.

## Dependencies
- None (foundation layer for all other modules).
